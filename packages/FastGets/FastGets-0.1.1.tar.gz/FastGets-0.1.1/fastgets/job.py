# coding: utf8

import sys
import time
from crontab import CronTab

from .core.errors import ApiError
from .utils import convert_path_to_name


def get_cron():
    return CronTab()


class Job(object):

    def __init__(self):
        self.id = None
        self.name = None
        self.trigger = None
        self.next_run_at = None

    def to_api_json(self):
        return dict(
            id=self.id,
            name=self.name,
            trigger=str(self.trigger),
            next_run_at=str(self.next_run_at)
        )

    @classmethod
    def get(cls, id):
        for job in cls.get_list():
            if job.id == id:
                return job

    @classmethod
    def get_by_name(cls, name):
        return cls.get_dict().get(name)

    @classmethod
    def add(cls, name, trigger):
        from fastgets.template import Template
        template = Template.get_dict().get(name)
        if not template:
            raise ApiError('名称不存在')

        if not trigger or trigger == '* * * * *':
            raise ApiError('trigger 非法')

        job_id = str(int(time.time()))
        cron = get_cron()
        each = cron.new(command='{} {} p'.format(sys.executable, template.path))
        each.setall(trigger)
        each.set_comment(job_id)
        if each.is_valid():
            each.enable()
            cron.write()
            return True
        else:
            return False

    def delete(self):
        cron = get_cron()
        for job in cron.find_comment(self.id):
            cron.remove(job)
            cron.write()

    @classmethod
    def get_list(cls):
        jobs = []
        for each in get_cron():
            splits = each.command.split()
            if len(splits) >= 2:
                continue
            path = splits[1]
            job = Job()
            job.id = each.comment
            job.name = convert_path_to_name(path)
            job.trigger = each.slices
            job.next_run_at = each.schedule().get_next()
            jobs.append(job)

        return jobs

    @classmethod
    def get_dict(cls):
        return {
            job.name: job
            for job in cls.get_list()
        }
