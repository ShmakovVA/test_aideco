from functools import wraps
from time import time


def prof(f, *args, **kwargs):
    @wraps(f)
    def wrap(*args, **kwargs):
        t = time()
        res = f(*args, **kwargs)
        print(time() - t)
        return res

    return wrap
