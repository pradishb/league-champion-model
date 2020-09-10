'''Loads a function only once'''
from functools import wraps


def load_once(function):
    '''
    Loads a function only once.
    Returns the same output after it has once once.
    The running can be reset by setting the `has_run` attribute to False
    '''
    output = None

    @wraps(function)
    def wrapper(*args, **kwargs):
        nonlocal output
        if not wrapper.has_run:
            output = function(*args, **kwargs)
            wrapper.has_run = True
        return output

    def reset():
        wrapper.has_run = False

    wrapper.has_run = False
    wrapper.reset = reset
    return wrapper
