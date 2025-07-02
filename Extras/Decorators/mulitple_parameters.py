def upper_decorator(*args):
    def inner_decorator(func):
        def wrapper():
            print(f"Argunments got {args}")
            print("before call")
            func()
            print("after call")
        return wrapper
    return inner_decorator

@upper_decorator("hello", 10)
def say_hello():
    print("Hello World")

say_hello()