# type: ignore
from pydantic import BaseModel
from rich import print

class Address(BaseModel):
    city: str
    zip_code: str

class User(BaseModel):
    name: str
    email: str
    address: Address  # Nested Model

#! Normal Example
user = User(
    name="Ali",
    email="ali@example.com",
    address=Address(city="Karachi", zip_code="1232")
)

print(user.address.city) 

#! Error Input should be a valid string [type=string_type, input_value=1232, input_type=int]
# user = User(
#     name="Ali",
#     email="ali@example.com",
#     address=Address(city="Karachi", zip_code=1232)
# )

# print(user.address.zip_code) 




class OrderItem(BaseModel):
    name: str
    quantity: int

class Order(BaseModel):
    order_id: int
    items: list[OrderItem]

order = Order(
    order_id="123",
    items=[
        {"name": "Sofa", "quantity": 1},
        {"name": "Table", "quantity": 2}
    ]
)

order.items.append({"name": "chair", "quantity": "2"})
order.items.append(OrderItem(name="chair", quantity="2"))
print(order)