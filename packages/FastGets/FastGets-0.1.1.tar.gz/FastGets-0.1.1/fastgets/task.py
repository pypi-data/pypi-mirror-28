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
from .utils import format_exception, create_id


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

    # 错误参数
    crawl_error_traceback = StringField()
    process_error_traceback = StringField()
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
            traceback_string = format_exception()
            raise CrawlError(traceback_string)

    def process(self, page_raw):
        try:
            self.func(self, page_raw)
        except Exception:
            traceback_string = format_exception()
            raise ProcessError(traceback_string)

    def _add_seed_task(self):
        from .pool import PendingPool

        assert not self.instance_id and env.instance_id
        self.instance_id = env.instance_id
        self.id = '{}_{}'.format(create_id(), self.instance_id)
        self.second_rate_limit = self.template_class.config.get('second_rate_limit', 30)

        while 1:
            if PendingPool.get_current_task_num(self.instance_id) >= \
                    self.template_class.config.get('max_pending_task_num', 1000):
                logger.debug('pending pool is full !')
                time.sleep(1)
            else:
                PendingPool.add(self)
                break

    def _add_new_task(self):
        pass

    def _add_retry_task(self):
        pass

    def _add_lost_task(self):
        pass

    def _add_manul_retry_task(self):
        # 在 api 中调用
        pass

    def _add_local_task(self):
        from .pool import PendingPool

        self.instance_id = env.instance_id
        self.id = '{}_{}'.format(create_id(), self.instance_id)
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
                elif reason == self.REASON_RETYR:
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
            raise FrameError('未知 mode')

    @classmethod
    def get(cls, id):
        assert id
        task_json = get_client().get(id)
        if task_json:
            return cls.from_json(task_json)

    def save(self, pipe=None):
        assert self.id
        client = pipe or get_client()
        client.set(self.id, self.to_json())
