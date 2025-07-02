def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                func(*args, **kwargs)
        return wrapper
    return decorator

#! Mushkil tareeka (but smjhny k liye acha ha)
def greet(name):
    print(f"Hello {name}")
decorator = repeat(3)
wrapper = decorator(greet)
wrapper("Fasih")


#! bht asaan tareeka
@repeat(8)
def say_hello(name):
    print(f"Hello to {name}")

say_hello("Ahmed")

