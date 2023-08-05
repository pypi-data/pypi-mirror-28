# coding: utf8

import redis
import mockredis
from .. import env


_client = None


def get_client():
    global _client
    if not _client:
        if env.mode == env.DISTRIBUTED:
            _config = dict(env.REDIS_CONFIG)
            _config['decode_responses'] = True
            _client = redis.Redis(**_config)
        else:
            _client = mockredis.MockRedis(decode_responses=True)

    return _client
