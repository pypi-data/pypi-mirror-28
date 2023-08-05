# coding: utf8

from ..core.client import get_client
from ..utils import to_hash


class CrawlErrorPool(object):

    @classmethod
    def add(cls, task):
        assert task.process_error_traceback

        client = get_client()

        key = '{}:crawl_error_pool'.format(task.instance_id)
        if client.llen(key) < 50:
            client.lpush(key, task.to_json())
            return

        key = '{}:crawl_error_hash_pool'.format(task.instance_id)
        hash_value = to_hash(task.process_error_traceback)
        if client.llen(key) > 50:
            # 避免异常情况
            return
        elif client.hexists(key, hash_value):
            # 同类错误已经存在
            return
        else:
            client.hset(key, hash_value, task.to_json())


class ProcessErrorPool(object):

    @classmethod
    def add(cls, task):
        assert task.process_error_traceback and task.page_raw

        client = get_client()

        key = '{}:process_error_pool'.format(task.instance_id)
        if client.llen(key) < 50:
            client.lpush(key, task.to_json())
            return

        key = '{}:process_error_hash_pool'.format(task.instance_id)
        hash_value = to_hash(task.process_error_traceback)
        if client.llen(key) > 50:
            # 避免异常情况
            return
        elif client.hexists(key, hash_value):
            # 同类错误已经存在
            return
        else:
            client.hset(key, hash_value, task.to_json())
