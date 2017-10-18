# -*- coding: utf-8 -*-
# Author: Forrest Chang (forrestchang7@gmail.com)

import code
import functools
import inspect
import re
import signal
import sys


def main(func):
    """
    Call func with command line argument. Used as a decorator.

    @main
    def main_function():
        pass

    Instead of using __name__ == '__main__'.
    """
    if inspect.stack()[1][0].f_locals['__name__'] == '__main__':
        args = sys.argv[1:]
        func(*args)
    return func


PREFIX = ''
def trace(func):
    """
    A decorator that prints a function's name, its arguments, and it's return values each time the
    function is called.

    @trace
    def test(arg):
        pass
    """
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        global PREFIX
        reprs = [repr(e) for e in args]
        reprs += [repr(k) + '=' + repr(v) for k, v in kwargs.items()]
        PREFIX += '    '
        try:
            result = func(*args, **kwargs)
            PREFIX = PREFIX[:-4]
        except Exception as e:
            log(func.__name__ + ' exited via exception')
            PREFIX = PREFIX[:-4]
            raise
        log('{0}({1}) -> {2}'.format(func.__name__, ', '.join(reprs), result))
        return result
    return wrapped


def log(message):
    """
    Print an indented message (used with trace).
    """
    if type(message) is not str:
        message = str(message)
    print(PREFIX + re.sub('\n', '\n' + PREFIX, message))


def log_current_line():
    """
    Print info about the current line of code.
    """
    frame = inspect.stack()[1]
    log('Current line: File "{f[1]}", line {f[2]}, in {f[3]}'.format(f=frame))

