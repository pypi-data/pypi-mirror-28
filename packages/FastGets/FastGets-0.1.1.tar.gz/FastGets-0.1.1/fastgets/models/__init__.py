from mongoengine import connect
from .instance import Instance
from .unknown_error_log import UnknownErrorLog
from .. import env

if env.mode == env.DISTRIBUTED:
    if env.configured:
        # 这里不能简单实用 mock 的方式，可能会影响到用户层项目
        connect(env.MONGO_CONFIG['db'], host=env.MONGO_CONFIG['host'], port=env.MONGO_CONFIG['port'])
    else:
        raise ValueError('must call fastgets.init_fastgets_env to init env')
