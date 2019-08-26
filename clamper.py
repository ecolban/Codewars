import math
from functools import wraps
from numbers import Number


def clamp(lo=None, hi=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            """Clamps the output of func"""
            y = func(*args, **kwargs)
            return lo if isinstance(lo, Number) and y < lo \
                else hi if isinstance(hi, Number) and y > hi \
                else y

        return wrapper

    return decorator


clamped_identity = clamp(lo=0, hi=1)(lambda x: x)


@clamp(-0.5, 0.5)
def clamped_sin(x):
    return math.sin(x)
