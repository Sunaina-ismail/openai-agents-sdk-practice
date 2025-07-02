
#! Asal ma ese run ho raha hota ha code
def decorator(func):
    def wrapper(*args, **kwargs):
        print("Function chalne se pehle")
        result = func(*args, **kwargs)
        print("Function chalne ke baad")
        return result
    return wrapper

def add(a, b):
    print(f"Result: {a + b}")
    return a + b

data = decorator(add)
data(10, 20)

#! Ham issy decorator k through bh bana skty hain

@decorator
def subtract(a, b):
    print(f"Result: {a - b}")
    return a - b

subtract(20, 2)