import datetime
from mongoengine import *
from ..utils import create_id, get_current_inner_ip


class UnknownErrorLog(Document):

    id = StringField()
    create_at = DateTimeField()
    traceback_string = StringField()
    inner_ip = StringField()

    meta = {
        'collection': 'fastgets_unknown_error_log'
    }

    @classmethod
    def add(cls, traceback_string):
        UnknownErrorLog.objects(id=create_id()).update(
            create_at=datetime.datetime.now(),
            traceback_string=traceback_string,
            inner_ip=get_current_inner_ip(),
            upert=True,
        )
