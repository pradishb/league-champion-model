'''Decorator that will postpone a function'''
from functools import wraps
from threading import Timer


def debounce(wait):
    '''
    Decorator that will postpone a functions
    execution until after wait seconds
    have elapsed since the last time it was invoked.
    '''
    def decorator(function):
        @wraps(function)
        def debounced(*args, **kwargs):
            def call_it():
                function(*args, **kwargs)
            try:
                debounced.t.cancel()
            except AttributeError:
                pass
            debounced.t = Timer(debounced.wait, call_it)
            debounced.t.daemon = True
            debounced.t.start()
        debounced.wait = wait
        return debounced
    return decorator
