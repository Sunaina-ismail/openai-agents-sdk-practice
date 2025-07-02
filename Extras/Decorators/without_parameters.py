
#? Simple example
#! Asal me ye hota ha 
def outer_function(func):
    def inner_function():
        print("Yeh kaam decorator ne kiya hai")
        func()
    return inner_function

def say_hello():
    print("Hello")

decorated = outer_function(say_hello)
decorated()

#! isko ham asa decorator bh use kr skty hain
@outer_function
def say_world():
    print("World")
