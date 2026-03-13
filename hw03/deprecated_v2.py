import warnings
from functools import wraps

def deprecated(a):
    def repeat(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            warnings.warn(a, UserWarning)
            return func(*args,**kwargs)
        return wrapper
    return repeat

@deprecated('Not pepe plz')
def mega_fun(x):
    print(x)

mega_fun(1)