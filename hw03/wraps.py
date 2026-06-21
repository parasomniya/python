import warnings
from functools import wraps

def wraps(func):
    def wrapper(*args,**kwargs):
        return func(*args,**kwargs)
    wrapper.__name__ = func.__name__
    wrapper.__module__ = func.__module__
    wrapper.__doc__ = func.__doc__
    return wrapper

@wraps
def zxc(x):
    print(x)

print(zxc.__name__)

import warnings
from functools import wraps

