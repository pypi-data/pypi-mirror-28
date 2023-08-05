# coding: utf8

import datetime
import os
import threading
import time

from .. import env
from ..stats import InstanceStats
from ..pool import RunningPoolMonitor, PendingPool
from ..utils import create_id, format_exception
from ..core.log import logger
from .base import Engine


class DistributedEngine(Engine):

    def __init__(self, template_class):
        self.template_class = template_class
        self.instance = self.make_instance()

        self.running_pool_monitor = RunningPoolMonitor(self.instance.id)

        self.running_pool_monitor_thread = None
        self.instance_update_thread = None
        self.seed_task_load_thread = None

        env.instance_id = self.instance.id

    def make_instance(self):
        from ..models.instance import Instance
        instance = Instance()
        instance.id = create_id()
        instance.process_id = str(os.getpid())
        instance.name = self.template_class.__name__
        instance.description = (self.template_class.__doc__ or '').strip()
        instance.start_at = datetime.datetime.now()
        instance.update_at = datetime.datetime.now()
        instance.save()

        return instance

    def sync_instance_from_mongo(self):
        from ..models.instance import Instance
        self.instance = Instance.objects.with_id(self.instance.id)
        assert self.instance

    def update_instance_from_redis(self):
        from ..models.instance import Instance

        task_ative_at, total_num, success_num, crawl_error_num, process_error_num, \
            avg_crawl_seconds, avg_process_seconds = InstanceStats.get(self.instance.id)

        pending_num = PendingPool.get_current_task_num(self.instance.id)

        Instance.objects(id=self.instance.id).update(
            set__task_active_at=task_ative_at,
            set__total_task_num=total_num,
            set__pending_task_num=pending_num,
            set__success_task_num=total_num,
            set__crawl_error_task_num=crawl_error_num,
            set__process_error_task_num=process_error_num,
            set__avg_crawl_seconds=avg_crawl_seconds,
            set__avg_process_seconds=avg_process_seconds,
            set__update_at=datetime.datetime.now(),
        )

    def start_running_pool_monitor_thread(self):
        def _():
            logger.info('monitor start')
            while self.instance.is_running():
                self.running_pool_monitor.loop()
                time.sleep(self.running_pool_monitor.CHECK_INTERVAL_SECONDS)

        self.running_pool_monitor_thread = threading.Thread(target=_)
        self.running_pool_monitor_thread.start()

    def start_instance_update_thread(self):
        def _():
            while self.instance.is_running():
                self.update_instance_from_redis()
                self.sync_instance_from_mongo()
                time.sleep(1)

        self.instance_update_thread = threading.Thread(target=_)
        self.instance_update_thread.start()

    def start_seed_task_load_thread(self):
        from ..models.instance import Instance

        def _():
            logger.info('load thread start')
            try:
                self.template_class.load()
            except Exception:
                traceback_string = format_exception()
                Instance.objects(id=self.instance.id).update(
                    set__traceback_string=traceback_string,
                    set__stop_at=datetime.datetime.now(),
                )
                logger.error('load thread error')

        self.seed_task_load_thread = threading.Thread(target=_, daemon=True)  # 由于无法主动中断 load 函数的执行 所以需要加 daemon
        self.seed_task_load_thread.start()

    def is_running(self):
        return self.running_pool_monitor_thread.is_alive() or \
               self.instance_update_thread.is_alive() or \
               (self.instance.is_running() and self.seed_task_load_thread.is_alive())

    def run(self):
        self.start_running_pool_monitor_thread()
        self.start_instance_update_thread()
        self.start_seed_task_load_thread()

        while self.is_running():
            time.sleep(1)
