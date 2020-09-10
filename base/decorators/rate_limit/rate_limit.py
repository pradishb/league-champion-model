'''Decorator that make functions not be called faster than the rate'''
import time
import threading
from functools import wraps


def rate_limit(min_interval, mode='kill', delay_first_call=False, on_error=None, debug=False):
    '''
    Decorator that make functions not be called faster than the rate

    set mode to 'kill' to just ignore requests that are faster than the
    rate.

    set delay_first_call to True to delay the first call as well
    '''
    lock = threading.Lock()

    def decorate(func):
        last_time_called = [0.0]

        last_sucess_value = None

        def get_on_error_value():
            if on_error is None:
                return False
            return on_error(last_sucess_value)

        def get_elapsed():
            return time.perf_counter() - last_time_called[0]

        def get_left_to_wait():
            return min_interval - get_elapsed()

        def get_is_rate_limited():
            return get_left_to_wait() > 0

        def run_func(args, kwargs):
            nonlocal last_sucess_value
            lock.release()
            ret = func(*args, **kwargs)
            last_time_called[0] = time.perf_counter()
            last_sucess_value = ret
            return ret

        @wraps(func)
        def rate_limited_function(*args, **kwargs):
            nonlocal last_sucess_value
            lock.acquire()
            if rate_limited_function.disabled:
                return run_func(args, kwargs)
            elapsed = get_elapsed()
            left_to_wait = min_interval - elapsed
            if delay_first_call:
                if left_to_wait > 0:
                    if mode == 'wait':
                        time.sleep(left_to_wait)
                        return run_func(args, kwargs)
                    lock.release()
                    if debug:
                        print(f'{func.__name__} rate limited')
                    return get_on_error_value()
                return run_func(args, kwargs)
            # Allows the first call to not have to wait
            if not last_time_called[0] or elapsed > min_interval:
                return run_func(args, kwargs)
            if mode == 'wait':
                time.sleep(left_to_wait)
                return run_func(args, kwargs)
            lock.release()
            if debug:
                print(f'{func.__name__} rate limited')
            return get_on_error_value()
        rate_limited_function.disabled = False
        rate_limited_function.get_is_rate_limited = get_is_rate_limited
        return rate_limited_function

    return decorate
