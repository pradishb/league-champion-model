'''Module for storing output decorator'''
from functools import wraps


def storeit(func):
    '''Decorator to store latest output'''
    output = None

    @wraps(func)
    def inner(*args, **kwargs):
        nonlocal output
        result = func(*args, **kwargs)
        output = result
        return result

    def get_last_output():
        return output

    inner.get_last_output = get_last_output
    return inner
