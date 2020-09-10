'''Decorator that make functions not be called faster than the rate'''
import os
import threading
import time
from functools import wraps

__all__ = ['rate_limit_persistent']

DIR_PATH = 'helper/rate_limit_persistent'


def _create_directories():
    os.makedirs(DIR_PATH, exist_ok=True)


def _load_last_called(function_name):
    file_path = os.path.join(DIR_PATH, function_name)
    if not os.path.isfile(file_path):
        return 0
    with open(file_path) as file_pointer:
        try:
            return float(file_pointer.read())
        except ValueError:
            return 0


def _save_last_called(function_name, last_called):
    file_path = os.path.join(DIR_PATH, function_name)
    with open(file_path, 'w') as file_pointer:
        file_pointer.write(str(last_called))


_create_directories()


def rate_limit_persistent(min_interval):
    '''
    Decorator that make functions not be called faster than the rate
    '''
    lock = threading.Lock()

    def decorate(func):
        last_called = _load_last_called(func.__name__)

        def run_func(args, kwargs):
            nonlocal last_called
            lock.release()
            output = func(*args, **kwargs)
            last_called = time.time()
            _save_last_called(func.__name__, last_called)
            return output

        @wraps(func)
        def wrapped_function(*args, **kwargs):
            lock.acquire()
            elapsed = time.time() - last_called
            if elapsed > min_interval:
                return run_func(args, kwargs)
            lock.release()
            return None
        return wrapped_function

    return decorate
