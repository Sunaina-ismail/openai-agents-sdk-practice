from typing import cast
from dataclasses import dataclass

@dataclass
class Student:
    _id: int
    name: str
    roll_no: int


@dataclass
class Teacher:
    name: str
    subject: str
    is_friendly: bool

student=Student(name="Muhammad Fasih", roll_no=123, _id=1)
teacher=Teacher(name="Sir Zia", subject="Agentic AI", is_friendly=True)

dummy = cast(Student, teacher)

#! Runs because actual object contains such key
print(dummy.subject)

#! Generate an error as there is no 'roll_no' in Teacher
print(dummy.roll_no)