# coding: utf8
import threading
import datetime
from mongoengine import *
from ..utils import datetime2utc
from ..core.decorators import sync

_cached_instance_ids = []
_cached_at = None


class Instance(Document):

    id = StringField(primary_key=True)
    process_id = StringField()
    name = StringField()
    description = StringField()
    start_at = DateTimeField()
    finish_at = DateTimeField()
    stop_at = DateTimeField()
    update_at = DateTimeField()

    total_task_num = IntField()
    pending_task_num = IntField()
    success_task_num = IntField()
    crawl_error_task_num = IntField()
    process_error_task_num = IntField()
    avg_crawl_seconds = FloatField()
    avg_process_seconds = FloatField()
    task_active_at = DateTimeField()

    traceback_string = StringField()

    meta = {
        'collection': 'fastgets_instance',
    }

    @property
    def status(self):
        if self.finish_at:
            return '已完成'
        elif self.stop_at:
            return '已停止'
        elif self.task_active_at and (datetime.datetime.now()-self.task_active_at).seconds < 10:
            return '正在运行'
        else:
            return '异常'

    def is_running(self):
        if self.stop_at or self.finish_at:
            return False
        return True

    def is_stopped(self):
        return bool(self.stop_at)

    @classmethod
    def get(cls, id):
        return cls.objects.with_id(id)

    def refresh(self):
        pass

    def stop(self):
        Instance.objects(id=self.id).update(set__stop_at=datetime.datetime.now())

    def finish(self):
        pass

    def to_api_json(self, **kwargs):
        task_active_at = None
        if self.task_active_at:
            if (datetime.datetime.now()-self.task_active_at).seconds <= 5:
                task_active_at = '刚刚'
            else:
                task_active_at = self.task_active_at.strftime('%m-%d %H:%M:%S')

        json_dict = dict(
            id=self.id,
            process_id=self.process_id,
            name=self.name,
            description=self.description,
            start_at=datetime2utc(self.start_at),
            finish_at=self.finish_at and datetime2utc(self.finish_at) or None,

            total_task_num=self.total_task_num,
            pending_task_num=self.pending_task_num,
            success_task_num=self.success_task_num,
            crawl_error_task_num=self.crawl_error_task_num,
            process_error_task_num=self.process_error_task_num,

            task_active_at=task_active_at,
            status=self.status,
        )
        json_dict.update(kwargs)
        return json_dict

    @classmethod
    @sync(threading.Lock())
    def get_running_ids(cls):
        global _cached_instance_ids, _cached_at
        now = datetime.datetime.now()
        if _cached_instance_ids and (now-_cached_at).seconds < 5:
            return _cached_instance_ids
        else:
            _cached_instance_ids = []
            _cached_at = now
            for each in cls.objects(
                    stop_at__exists=False, update_at__gte=now-datetime.timedelta(seconds=30)
            ).only('id').as_pymongo().no_cache():
                _cached_instance_ids.append(each['_id'])
            return _cached_instance_ids

