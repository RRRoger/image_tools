# -*- coding: utf-8 -*-

from functools import wraps
import time


def time_cost(func):
    """
    :param func: function
    :return: 计算函数耗时多久
    """
    @wraps(func)
    def _wrapper(*args, **kwargs):
        now = time.time()
        res = func(*args, **kwargs)
        log_txt = u'函数 %s 耗时 %.2fs!' % (func.__name__, time.time() - now)
        print(log_txt)
        return res
    return _wrapper