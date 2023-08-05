# coding: utf8

import re
import lxml.html
from ..core.errors import ParseError


INT_PATTERN = re.compile('[0-9]]+')
FLOAT_PATTERN = re.compile('[0-9\.]+')


def parse_doc(html):
    return lxml.html.fromstring(html)


def parse_int(s):

    for each in INT_PATTERN.findall(s):
        try:
            return int(each)
        except ValueError:
            pass

    raise ParseError('cant parse int from {}'.format(s))


def parse_float(s):

    for each in FLOAT_PATTERN.findall(s):
        try:
            return float(each)
        except ValueError:
            pass

    raise ParseError('cant parse float from {}'.format(s))
