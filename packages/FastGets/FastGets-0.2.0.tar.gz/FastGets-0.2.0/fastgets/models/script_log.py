# coding: utf8

from mongoengine import *


class ScriptLog(Document):

    id = StringField(primary_key=True)
    name = StringField()
    start_at = DateTimeField()
    end_at = DateTimeField()
    traceback = ListField(StringField())

    meta = {
        'collection': 'fastgets_script_log'
    }
