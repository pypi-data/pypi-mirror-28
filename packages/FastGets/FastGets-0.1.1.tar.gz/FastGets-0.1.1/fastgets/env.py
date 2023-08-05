# coding: utf8


TEST = 'test'
LOCAL = 'local'
DISTRIBUTED = 'distributed'
API = 'api'

mode = None
is_loading_seed_tasks = False
instance_id = None

configured = False

REDIS_CONFIG, MONGO_CONFIG, API_CONFIG, PROJECT_ROOT_DIR, TEMPLATES_DIR = [None] * 5
