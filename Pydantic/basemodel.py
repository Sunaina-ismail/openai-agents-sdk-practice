from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str

#! Basic Example
user = User(id=1, name="Ali", email="ali@example.com")

print(user)
print(user.name)


#! Error: Input should be a valid integer, unable to parse string as an integer
dummy_user = User(id="fake", name="Ahmed", email="ahmed123@gmail.com")  
print(dummy_user)



from typing import Optional

class AnotherUser(BaseModel):
    id: int
    name: str
    email: Optional[str] = None

one_more_user=AnotherUser(id=2, name="Ahmed")
print(one_more_user.email)