# coding: utf8

import os
import subprocess
import psutil
from .core.errors import ApiError
from .utils import utc2datetime
from . import env


class Process(object):

    def __init__(self):
        self.id = None
        self.name = None
        self.path = None
        self.template_name = None
        self.memory_percent = None
        self.thread_num = None
        self.create_at = None
        self._process = None

    @property
    def cpu_percent(self):
        return self._process.cpu_percent(interval=0.1)

    def kill(self):
        self._process.kill()

    def to_api_json(self):
        return dict(
            id=self.id,
            name=self.name,
        )

    @classmethod
    def add(cls, name):
        from fastgets.template import Template

        if name in cls.get_dict():
            raise ApiError('不能重复启动')

        template = Template.get_dict().get(name)
        if not template:
            raise ApiError('模板名不存在')

        cmdline = ['python3', template.path, 'p']
        dev_null = open(os.devnull, 'wb')
        subprocess.Popen(
            cmdline,
            stdout=dev_null, stderr=dev_null, stdin=dev_null, close_fds=True
        )

    @classmethod
    def is_fastgets(cls, _process):
        try:
            cmdline = _process.cmdline()
            if len(cmdline) >= 2 and _process.name() == 'Python' and env.TEMPLATES_DIR in cmdline[1]:
                return True
        except psutil.AccessDenied:
            pass

        return False

    @classmethod
    def _get(cls, _process):
        process = Process()
        process.id = str(_process.pid)
        process.path = _process.cmdline()[1]
        process.name = process.path.split(env.TEMPLATES_DIR)[-1][:-len('.py')]
        process.memory_percent = _process.memory_percent
        process.thread_num = _process.num_threads()
        process.create_at = utc2datetime(_process.create_time())
        process._process = _process
        return process

    @classmethod
    def get(cls, id):
        _process = psutil.Process(int(id))
        return cls._get(_process)

    @classmethod
    def get_list(cls):
        process_list = []
        for pid in psutil.pids():
            _process = psutil.Process(pid)
            if cls.is_fastgets(_process):
                process_list.append(cls._get(_process))

        return process_list

    @classmethod
    def get_dict(cls):
        return {
            process.id: process
            for process in cls.get_list()
        }
