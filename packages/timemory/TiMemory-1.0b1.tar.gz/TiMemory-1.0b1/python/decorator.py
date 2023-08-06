#!/usr/bin/env python

def auto_timer_decorator(function):

    """
    Limits how fast the function is
    called.
    """
    def wrapper(*args, **kwargs):
        autotimer = tim.auto_timer('{}:{}'.format(tim.FILE(), tim.LINE()),
                                   nback=3)
        return function(*args, **kwargs)
    return wrapper
