import logging
from datetime import timedelta
from functools import wraps
from time import time

LOGGER = logging.getLogger(__name__)


def benchmark(prefix=""):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time()
            result = func(*args, **kwargs)
            end = time()
            delta = timedelta(seconds=(end - start))
            LOGGER.info(f"{prefix}{func.__name__}(...) took {delta}")
            return result

        return wrapper

    return decorator
