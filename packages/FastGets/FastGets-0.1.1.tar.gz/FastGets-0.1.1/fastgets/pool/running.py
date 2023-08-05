# coding: utf8
import time

from ..core.client import get_client
from ..core.errors import FrameError
from ..task import Task


class RunningPool(object):

    @classmethod
    def create_key(cls, instance_id):
        return '{}:{}'.format('running_pool', instance_id)

    @classmethod
    def get_task_ids(cls, instance_id):
        return get_client().lrange(cls.create_key(instance_id), 0, -1)

    @classmethod
    def remove(cls, instance_id, task_id):
        get_client().lrem(
            cls.create_key(instance_id),
            task_id,
            num=1  # 不直接用默认值 1 可以提高一点性能
        )


class RunningPoolMonitor(object):

    CHECK_INTERVAL_SECONDS = 10
    MAX_RUNNING_SECONDS = 20

    def __init__(self, instance_id):
        self.instance_id = instance_id
        self.add_time_dict = {}  # task_id: time

    def loop(self):
        now = time.time()
        old_add_time_dict = self.add_time_dict
        self.add_time_dict = {}

        running_task_ids = RunningPool.get_task_ids(self.instance_id)
        for task_id in set(old_add_time_dict.keys()) & set(running_task_ids):
            add_time = old_add_time_dict[task_id]
            if (now - add_time) > self.MAX_RUNNING_SECONDS:
                # 超出最大运行时间，任务应该是没有正常结束
                task = Task.get(task_id)
                if not task:
                    raise FrameError('task 不存在')
                task.add(reason='missing')
            else:
                self.add_time_dict[task_id] = add_time

        for task_id in set(old_add_time_dict.keys()) - set(running_task_ids):
            self.add_time_dict[task_id] = now

    def is_ready_to_finish(self):
        return not bool(self.add_time_dict)
