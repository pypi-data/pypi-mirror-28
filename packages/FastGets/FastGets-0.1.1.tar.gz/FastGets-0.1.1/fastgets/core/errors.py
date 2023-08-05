
from werkzeug.exceptions import HTTPException
from flask import jsonify


class ApiError(HTTPException):

    def __init__(self, msg='', code=1):
        HTTPException.__init__(self)
        self.response = jsonify(dict(error_code=code, error_msg=msg))


class CrawlError(Exception):

    def __init__(self, traceback_string):
        self.traceback_string = traceback_string


class ProcessError(Exception):

    def __init__(self, traceback_string):
        self.traceback_string = traceback_string


class WriteError(Exception):
    pass


class NotSupported(Exception):
    pass


class ParseError(Exception):
    pass


class FrameError(Exception):
    pass
