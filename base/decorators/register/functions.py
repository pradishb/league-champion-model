

registry = {}


def get_registry(key):
    return registry.get(key, None)


def register(*args):
    def _register(func):
        registry[func.__name__] = func, args

        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return _register
