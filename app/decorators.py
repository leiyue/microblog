# -*- coding: utf-8 -*-
# @Date    : 2016-01-23 21:40
# @Author  : leiyue (mr.leiyue@gmail.com)
# @Link    : https://leiyue.wordpress.com/


def async(func):
    from threading import Thread
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        thr = Thread(target=func, args=args, kwargs=kwargs)
        thr.start()
        return thr

    return wrapper
