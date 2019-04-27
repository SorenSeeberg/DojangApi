#!/usr/bin/python3
# -*- coding: utf-8 -*-


class _Exception(Exception):

    def __init__(self, msg: str):
        Exception.__init__(self, msg)


class Exceptions:

    class DuplicateEmailError(_Exception):
        def __init__(self):
            _Exception.__init__(self, f'{self.__class__.__name__}: Email already exist in database')

    class EmailNotFoundError(_Exception):
        def __init__(self):
            _Exception.__init__(self, f'{self.__class__.__name__}: Email doesn''t exist in database')

    class Unauthorized(_Exception):
        def __init__(self):
            _Exception.__init__(self, f'{self.__class__.__name__}: 401')
