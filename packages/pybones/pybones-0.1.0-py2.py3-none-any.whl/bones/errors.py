# -*- coding: utf-8 -*-


class BaseError(Exception):
    """Base exception for bones package"""
    def __init__(self, message=None, *args, **kwds):
        if message is not None:
            message = message.format(**kwds) if kwds else message
        else:
            message = self.__doc__.format(**kwds) if kwds else self.__doc__
        self.__msg__ = message
        Exception.__init__(self, message)

    def __str__(self):
        return self.__msg__


class APIError(BaseError):
    """Organizational Abstract Error for API errors."""


class CLIError(BaseError):
    """Organizational Abstract Error for Command Line Interface errors."""


class InvalidURLError(APIError):
    """URL is not accessible: {url}"""


class PythonVersionMismatch(CLIError):
    """Python version not found: {version}"""
