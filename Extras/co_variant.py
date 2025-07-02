from typing import TypeVar, Generic

class Animal: pass
class Dog(Animal): pass

T_co = TypeVar("T_co", covariant=True)

class ReadOnlyBox(Generic[T_co]):
    def __init__(self, value: T_co):
        self.value = value

    def get(self) -> T_co:
        return self.value

dog=Dog()
dog_box = ReadOnlyBox(dog)       # ✅ yeh box Dog ka hai
animal_box: ReadOnlyBox[Animal] = dog_box  # ✅ allowed because T_co is covariant

print(isinstance(animal_box.get(), Animal))  # ✅ True


T_contra = TypeVar("T_contra", contravariant=True)

class OneMoreReadOnlyBox(Generic[T_contra]):
    def __init__(self, value: T_contra):
        self.value = value

    def get(self) -> T_contra:
        return self.value

animal=Animal()
one_more_animal_box: OneMoreReadOnlyBox[Animal] = OneMoreReadOnlyBox(animal)
one_more_dog_box: OneMoreReadOnlyBox[Dog] = one_more_animal_box

