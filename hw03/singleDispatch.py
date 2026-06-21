from functools import singledispatch

@singledispatch
def zxc(x):
    print("fa")

@zxc.register
def _(x: int):
    print(x, "wtfa")

@zxc.register
def _(x: str):
    print(x, "fa fa")

zxc(1)
zxc([1,2,3])