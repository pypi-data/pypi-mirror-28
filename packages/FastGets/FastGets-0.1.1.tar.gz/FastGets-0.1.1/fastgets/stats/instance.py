# coding: utf8

import time
import datetime
from ..core.client import get_client
from ..utils import utc2datetime
from ..task import Task


class InstanceStats(object):

    @classmethod
    def check_rate_limit(cls, instance_id, second_rate_limit):
        now = datetime.datetime.now()
        key = '{}:rate_limit'.format(instance_id)
        field = now.strftime('%Y%m%d%H%M%S')
        if second_rate_limit < get_client().hincrby(key, field):
            return True
        else:
            return False

    @classmethod
    def set_task_active(cls, instance_id, pipe=None):
        client = pipe or get_client()
        client.set('{}:task_ative_at'.format(instance_id), int(time.time()))  # 精确到秒就行了

    @classmethod
    def add(cls, instance_id, name, pipe=None):
        # name: total success process_error crawl_error
        client = pipe or get_client()
        client.hincrby('{}:num_stats'.format(instance_id), name)

    @classmethod
    def add_time_cost(cls, task, crawl_seconds, process_seconds, pipe=None):
        # name: crawl process
        client = pipe or get_client()

        # 分别统计抓取和处理的总耗时
        client.hincrbyfloat('{}:time_stats'.format(task.instance_id), 'crawl', crawl_seconds)
        client.hincrbyfloat('{}:time_stats'.format(task.instance_id), 'process', process_seconds)

        task_json = task.to_json()

        key = '{}:crawl_seconds_ranking'.format(task.instance_id)
        client.zadd(key, task_json, -crawl_seconds)  # 确保大的排前面
        # todo 这里直接存储整个 json ，性能肯能有问题
        client.zremrangebyrank(key, 10, -1)  # 只保存 TOP 10

        key = '{}:process_seconds_ranking'.format(task.instance_id)
        client.zadd(key, task_json, -process_seconds)
        client.zremrangebyrank(key, 10, -1)

    @classmethod
    def get_top_tasks(cls, instance_id):
        # todo 没想到更好的名字
        client = get_client()
        with client.pipeline() as pipe:
            pipe.zrange('{}:crawl_seconds_ranking'.format(instance_id), 0, 10)
            pipe.zrange('{}:process_seconds_ranking'.format(instance_id), 0, 10)
            crawl_tasks, process_tasks = pipe.execute()
            crawl_tasks = [
                Task.from_json(each)
                for each in crawl_tasks
            ]
            process_tasks = [
                Task.from_json(each)
                for each in process_tasks
            ]
        return crawl_tasks, process_tasks

    @classmethod
    def get(cls, instance_id):
        with get_client().pipeline() as pipe:
            pipe.get('{}:task_ative_at'.format(instance_id))
            pipe.get('{}:num_stats'.format(instance_id))
            pipe.hgetall('{}:time_stats'.format(instance_id))
            task_ative_at, num_stats, time_stats = pipe.execute()

            if task_ative_at:
                task_ative_at = utc2datetime(int(task_ative_at))

            num_stats = num_stats or {}
            total_num = int(num_stats.get('total') or 0)
            success_num = int(num_stats.get('success') or 0)
            crawl_error_num = int(num_stats.get('crawl_error') or 0)
            process_error_num = int(num_stats.get('process_error') or 0)

            avg_crawl_seconds = None
            avg_process_seconds = None
            if success_num:
                avg_crawl_seconds = time_stats['crawl'] / success_num
                avg_process_seconds = time_stats['process'] / success_num

            return task_ative_at, total_num, success_num, crawl_error_num, process_error_num, \
                avg_crawl_seconds, avg_process_seconds
