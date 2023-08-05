# coding: utf8

__version__ = '0.1.1'

from .task import Task
from .template import TemplateBase
from .writer import CsvWriter
from .core import init_fastgets_env

from .core.log import logger  # 触发 logging 配置
