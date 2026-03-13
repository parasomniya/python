import warnings
from functools import wraps

def mock(return_value):
    def repeat(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            print(return_value)
        return wrapper
    return repeat

@mock("shnele")
def zxc(x):
    print(x)

zxc(1)