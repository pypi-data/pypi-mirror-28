#! coding:utf-8


class FailureException(Exception):
    '''This class mainly used for __bool__,
        self.error for reviewing the source exception.'''

    def __init__(self, error):
        self.__dict__ = error.__dict__
        self.error = error
        self.ok = False

    def __bool__(self):
        return False

    def __nonzero__(self):
        return False

    def __str__(self):
        return repr(self)
