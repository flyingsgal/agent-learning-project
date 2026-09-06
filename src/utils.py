import time
from functools import wraps

#wrapper 虽然负责包裹原函数，但要把原函数的重要元信息保留下来。使用@wraps(func)保留装饰前的函数名
#decorator标准模板
def decorator(func):
    @wraps(func) 
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result
    return wrapper


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()

        result = func(*args, **kwargs)

        end = time.perf_counter()
        print(
            f"{func.__name__} took "
            f"{end - start:.6f}s"
        )
        return result
    return wrapper