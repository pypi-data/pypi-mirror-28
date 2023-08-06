"""
    A package for timeout
    This script can be used both as decorator or
    a context in codes.

    Example:
    @timeout(10, 'Your script timed out')
    def funct():
        while True:
            print 'Hello world!'

    OR

    with timeout(10, 'Your loop timedout'):
        while True:
            print 'Hello world!'
"""

import signal


class TimeoutError(Exception):
    pass


class timeout(object):
    def __init__(self, timeout=10, message="Timed out"):
        self.timeout = timeout
        self.message = message

    def raise_timeout_exception(self, signum, frame):
        raise TimeoutError(self.message)

    def create_signal(self):
        signal.signal(signal.SIGALRM, self.raise_timeout_exception)
        signal.alarm(self.timeout)

    def stop_signal(self):
        signal.alarm(0)

    def __enter__(self):
        self.create_signal()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_signal()

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            with self:
                return func(*args, **kwargs)
        return wrapper
