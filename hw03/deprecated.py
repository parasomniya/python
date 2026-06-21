import warnings
from functools import wraps

def deprecated(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        warnings.warn("not pepe", UserWarning)
        return func(*args,**kwargs)
    return wrapper

@deprecated
def zxc(x):
    print(x)

zxc(1)