# coding: utf8

from .core.log import logger  # 触发 logging 配置

from .task import Task
from .template import TemplateBase
from .writer import CsvWriter
from .core import init_fastgets_env
from .parse import parser, parse_doc, parse_float, Site, ParseItem, parse_node_text, parse_node_html, parse_time


__version__ = '0.1.4'
