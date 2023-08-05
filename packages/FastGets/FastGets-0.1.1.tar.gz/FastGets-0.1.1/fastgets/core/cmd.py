import argparse
from werkzeug.utils import import_string
from .. import env


def init_fastgets_env(config):
    # todo 合法性检查
    env.REDIS_CONFIG = config.REDIS_CONFIG
    env.MONGO_CONFIG = config.MONGO_CONFIG
    env.API_CONFIG = config.API_CONFIG
    env.PROJECT_ROOT_DIR = config.PROJECT_ROOT_DIR
    env.TEMPLATES_DIR = config.TEMPLATES_DIR
    env.configured = True


def mode_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-m', '--mode', choices=['t', 'l', 'd'], default='l',
        help='1) t - test 2) l - local 3) d - distributed . local is default')
    args = parser.parse_args()

    env.mode = dict(
        t=env.TEST,
        l=env.LOCAL,
        d=env.DISTRIBUTED,
    )[args.mode]


def config_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='config path. for example, myproject.config')
    args = parser.parse_args()

    config = import_string(args.config)
    init_fastgets_env(config)
