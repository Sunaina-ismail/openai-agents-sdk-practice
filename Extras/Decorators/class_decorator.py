class MyDecorator:
    def __init__(self, func):
        print("Init function executed")
        self.func = func

    def __call__(self, *args, **kwargs):
        print("Before function call")
        result = self.func(*args, **kwargs)
        print("After function call")
        return result

#! Normally ese chalta ha
def greet():
    print("Hello World")
obj = MyDecorator(greet)
obj()

print("\n")

@MyDecorator
def say_hello(name):
    print(f"Hello {name}")

say_hello("Fasih")