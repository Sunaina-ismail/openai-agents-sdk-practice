class Printer:
    def __str__(self):
        return "Such a beautiful class"
    
a=Printer()
print(a)

class Maths:
    def __call__(self, *data):
        return sum(data)
    
calculator=Maths()
sum=calculator(14,35,46,57,5)
print(sum)


class User:
    def __init__(self, name):
        self.name = name

user=User("Muhamamd Fasih")
print(user.name)
