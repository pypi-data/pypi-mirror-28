# coding: utf8
import time
import sys
import requests
from werkzeug.utils import import_string
from mongoengine import *

from . import env
from .core.log import logger
from .core.errors import CrawlError, ProcessError, FrameError
from .core.client import get_client
from .utils import format_exception, create_id, time_readable
from .stats import InstanceStats


class Task(Document):

    GET = 'GET'
    POST = 'POST'

    REASON_SEED = 'seed'
    REASON_NEW = 'new'
    REASON_RATE_LIMIT = 'rate_limit'
    REASON_LOST = 'lost'
    REASON_RETYR = 'retry'
    REASON_MANUL_RETRY = 'manul_retry'

    id = StringField(primary_key=True)

    # instance相关
    instance_id = StringField()

    # 抓取相关
    headers = DictField()
    url = URLField()
    method = StringField(default='GET')
    get_payload = DictField()
    post_payload = DictField()
    encoding = StringField()
    timeout = IntField(default=5)
    current_retry_num = IntField(default=0)
    max_retry_num = IntField(default=3)

    # 处理相关
    template_class_path = StringField()
    func_name = StringField()
    temp_data = DictField()

    # 速度控制
    second_rate_limit = IntField()

    # 执行过程
    start_at = DateTimeField()
    end_at = DateTimeField()
    crawl_seconds = FloatField()
    process_seconds = FloatField()

    # 错误参数
    crawl_error_traceback = ListField(StringField())
    process_error_traceback = ListField(StringField())
    page_raw = StringField()

    # 其它
    add_reason = StringField()

    @property
    def template_class(self):
        return import_string(self.template_class_path)

    @property
    def func(self):
        func = getattr(self.template_class, self.func_name)
        return func

    @func.setter
    def func(self, func):
        self.func_name = func.__name__
        template_class = func.__self__

        module = template_class.__module__
        if env.mode == env.DISTRIBUTED and env.is_loading_seed_tasks:
            path = sys.argv[0][:-3]  # 去除 .py 后缀
            if env.PROJECT_ROOT_DIR in path:
                path = path.split(env.PROJECT_ROOT_DIR)[1]
            module = path.replace('/', '.')

        self.template_class_path = '{}:{}'.format(module, template_class.__name__)

    def new(self):
        task = Task.from_json(self.to_json())
        del task.id
        del task.add_reason

        if env.mode == env.DISTRIBUTED and env.is_loading_seed_tasks:
            # 分布式模式下 加载种子任务时需要确保 instance_id 为空
            del task.instance_id

        return task

    def _prepare_kwds(self):
        kwds = {
            'timeout': self.timeout,
            'headers': self.headers,
        }
        return kwds

    def _get_crawl(self):
        kwds = self._prepare_kwds()
        if self.get_payload:
            kwds['params'] = self.get_payload

        r = requests.get(self.url, **kwds)
        if self.encoding:
            r.encoding = self.encoding
        return r.text

    def _post_crawl(self):
        kwds = self._prepare_kwds()
        if self.post_payload:
            kwds['data'] = self.post_payload

        r = requests.post(self.url, **kwds)
        if self.encoding:
            r.encoding = self.encoding
        return r.text

    def crawl(self):
        try:
            if self.method == self.GET:
                return self._get_crawl()
            elif self.method == self.POST:
                return self._post_crawl()
            else:
                raise ValueError('error method')
        except Exception:
            self.current_retry_num += 1
            if self.current_retry_num <= self.max_retry_num:
                self.add(reason=self.REASON_RETYR)

            self.current_retry_num -= 1  # 还原初始值
            raise CrawlError(format_exception())

    def process(self, page_raw):
        try:
            self.func(self, page_raw)
        except Exception:
            raise ProcessError(format_exception())

    def _add_seed_task(self):
        from .pool import PendingPool

        assert not self.instance_id and env.instance_id
        self.instance_id = env.instance_id
        self.create_id()
        self.second_rate_limit = self.template_class.config.get('second_rate_limit', 30)

        while 1:
            if PendingPool.get_current_task_num(self.instance_id) >= \
                    self.template_class.config.get('max_pending_task_num', 1000):
                logger.debug('pending pool is full !')
                time.sleep(1)
            else:
                PendingPool.add(self)
                InstanceStats.incr(self.instance_id, 'total')
                break

    def _add_new_task(self):
        from .pool import PendingPool

        assert self.instance_id
        self.create_id()
        PendingPool.add(self)
        InstanceStats.incr(self.instance_id, 'total')

    def _add_rate_limit_task(self):
        from .pool import PendingPool

        assert self.instance_id
        PendingPool.add(self)

    def _add_retry_task(self):
        from .pool import PendingPool

        assert self.instance_id
        PendingPool.add(self)

    def _add_lost_task(self):
        from .pool import PendingPool

        assert self.instance_id
        PendingPool.add(self)

    def _add_manul_retry_task(self):
        # 在 api 中调用
        from .pool import PendingPool

        assert self.instance_id
        PendingPool.add(self)

    def _add_local_task(self):
        from .pool import PendingPool

        self.instance_id = env.instance_id
        self.create_id()
        self.second_rate_limit = self.template_class.config.get('second_rate_limit', 10)
        PendingPool.add(self)

    def add(self, reason=None):

        if env.mode == env.DISTRIBUTED:
            if env.is_loading_seed_tasks:
                # template
                if reason == self.REASON_LOST:
                    self.add_reason = self.REASON_LOST
                    self._add_lost_task()
                else:
                    assert reason is None
                    self.add_reason = self.REASON_SEED
                    self._add_seed_task()
            else:
                # worker
                if reason is None:
                    self.add_reason = self.REASON_NEW
                    self._add_new_task()
                elif reason == self.REASON_RATE_LIMIT:
                    self.add_reason = self.REASON_RATE_LIMIT
                    self._add_rate_limit_task()
                elif reason == self.REASON_RETYR:
                    self.add_reason = self.REASON_RATE_LIMIT
                    self._add_retry_task()
                else:
                    raise FrameError('unknown reason')

        elif env.mode == env.API:
            assert reason == self.REASON_MANUL_RETRY
            self.add_reason = self.REASON_MANUL_RETRY
            self._add_manul_retry_task()

        elif env.mode in [env.LOCAL, env.TEST]:
            self._add_local_task()
        else:
            raise FrameError('unknown mode')

    def create_id(self):
        assert not self.id
        assert self.instance_id
        self.id = '{}_{}'.format(self.instance_id, create_id())

    @classmethod
    def get(cls, id):
        assert id
        task_json = get_client().get(id)
        if task_json:
            return cls.from_json(task_json)

    @classmethod
    def gets(cls, ids):
        if not ids:
            return []

        task_json_list = filter(None, get_client().mget(ids))
        return [
            Task.from_json(task_json)
            for task_json in task_json_list
        ]

    def save(self, pipe=None):
        assert self.id
        client = pipe or get_client()
        client.set(self.id, self.to_json())

    def to_api_json(self):
        return dict(
            id=self.id,
            func_name=self.func_name,
            url=self.url,
            method=self.method,
            get_payload=self.get_payload,
            post_payload=self.post_payload,
            temp_data=self.temp_data,
            crawl_seconds=self.crawl_seconds and round(self.crawl_seconds, 2) or None,
            process_seconds=self.process_seconds and round(self.process_seconds, 2) or None,
            error_traceback=self.crawl_error_traceback or self.process_error_traceback,
        )
