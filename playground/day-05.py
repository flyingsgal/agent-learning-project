def decorator(func):
    def wrapper(*args, **kwargs):
        print("before")
        result = func(*args, **kwargs)
        print("after")
        return result
    return wrapper

@decorator
def hello():
    print("hello")
    
@decorator
def add(a,b):
    return a+b
# hello()
# print(add(1,2))

import time
def timer(func):
    def wrapper(*arg,**kwargs):
        start = time.perf_counter()
        result = func(*arg,**kwargs)
        end = time.perf_counter()
        print(
            f"{func.__name__} took "
            f"{end - start:.6f}s"
        )
        return result
    return wrapper
@timer
def add(a, b):
    return a + b
# print(add(1, 2)) #原函数名字add，wrapper名字wrapper，装饰后add的名字wrapper


class DemoContext:
    def __enter__(self):
        print("进入 context")
        return self
    def __exit__(self, exc_type, exc_value, traceback): #返回值决定发生的异常要不要继续往外抛。默认return None，也就是False，不吞掉异常
        print("退出 context")
        print("exc_type:", exc_type)
        print("exc_value:", exc_value)
        return True
with DemoContext() as ctx: #ctx接收enter的返回self
    print("正在执行代码")
    #即使发生错误，exit依旧执行
    0/0 
print("继续执行")