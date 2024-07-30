import functools
import warnings
from datetime import datetime
from decimal import Decimal


def deprecated(reason):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(
                f"{func.__name__} is deprecated: {reason}",
                category=DeprecationWarning,
                stacklevel=2,
            )
            return func(*args, **kwargs)

        return wrapper

    return decorator


def num_to_str(value):
    if isinstance(value, int):
        return str(value)
    elif isinstance(value, Decimal):
        if value % 1 == 0:
            return str(int(value))
        else:
            return str(value)
    else:
        return value


def bool_to_str(value):
    if isinstance(value, str):
        value = value.replace("True", "1")
        value = value.replace("False", "0")
    return value


def time_to_str(value):
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    return value