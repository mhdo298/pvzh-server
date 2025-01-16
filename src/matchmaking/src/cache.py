import os
import time
from redis import Redis, exceptions

r = Redis.from_url(os.getenv('REDIS_URL'))


def get_or_default(param, method, default=None, attempts=10, timeout=0.5):
    error = None
    for _ in range(attempts):
        try:
            res = method(param)
            if res is not None:
                return res
        except exceptions.ConnectionError as exc:
            error = exc
        time.sleep(timeout)
    if default is None:
        if error is not None:
            raise error
    return default
