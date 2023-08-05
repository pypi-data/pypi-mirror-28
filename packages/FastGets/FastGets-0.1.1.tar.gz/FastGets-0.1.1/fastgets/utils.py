# coding: utf8

import uuid
import hashlib
import time
import datetime
import threading
import socket
import sys
import traceback
from . import env


def create_id():
    return str(uuid.uuid4()).replace('-', '')[:16]


def to_hash(*args):
    m = hashlib.md5()
    for arg in args:
        m.update(str(arg))
    return m.hexdigest()


def datetime2utc(dt):
    return int(time.mktime(dt.timetuple()))


def utc2datetime(t):
    return datetime.datetime.fromtimestamp(t)


def format_exception():
    exception_list = traceback.format_stack()
    exception_list = exception_list[:-2]
    exception_list.extend(traceback.format_tb(sys.exc_info()[2]))
    exception_list.extend(
        traceback.format_exception_only(
            sys.exc_info()[0], sys.exc_info()[1]
        )
    )

    exception_str = "Traceback (most recent  call last):\n"
    exception_str += "".join(exception_list)
    # Removing the last \n
    exception_str = exception_str[:-1]

    return exception_str[-1000:]


def get_current_inner_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def get_thread_name():
    return threading.current_thread().name


def convert_path_to_name(path):
    if env.TEMPLATES_DIR not in path:
        return

    file_name = path.split(env.TEMPLATES_DIR)[-1]
    if file_name == '__init__.py':
        return

    if not file_name.endswith('.py'):
        return

    return file_name[:-len('.py')]


def convert_name_to_path(name):
    return '{}{}.py'.format(env.TEMPLATES_DIR, name)
