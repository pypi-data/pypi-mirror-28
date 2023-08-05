# coding:utf-8
__author__ = 'zhoukunpeng'
# --------------------------------
# Created by zhoukunpeng  on 2015/8/15.
# ---------------------------------

def singlon(fun):
    "单例模式装饰器"
    instance={}
    def wappedfun(*args,**kwargs):
        if instance.has_key(fun):
            pass
        else:
            instance[fun]=fun(*args,**kwargs)
        return  instance[fun]
    return wappedfun

class Singleton(type):
    def __init__(self, name, bases, dict):
        super(Singleton, self).__init__(name, bases, dict)
        self._instance = None
    def __call__(self, *args, **kw):
        if self._instance is None:
            self._instance = super(Singleton, self).__call__(*args, **kw)
        return self._instance