from typing import overload

#! Overload signatures — sirf IDE ke liye
@overload
def greet(name: str) -> str: ...

@overload
def greet(name: str, age: int) -> str: ...

#! Real implementation
def greet(name, age=None):
    if age is None:
        return f"Hello {name}"
    return f"Hello {name}, you are {age}"


print(greet("Fasih"))       #? ✅ IDE samjhega: str input → str output
print(greet("Fasih", 25))   #? ✅ IDE samjhega: str + int → str output
