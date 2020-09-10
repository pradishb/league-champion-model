'''Decorator to time a function'''
import time
import json
import os



disabled = os.environ.get('DISABLE_TIMEIT', 'False') == 'True'


def timeit(method):
    '''Decorator to time a function'''
    def timed(*args, **kwargs):
        if disabled:
            return method(*args, **kwargs)
        start = time.time()
        result = method(*args, **kwargs)
        end = time.time()
        print(f'{method.__name__} {(end - start)*1000}ms')
        return result
    return timed
