from pydantic import BaseModel, Field
from rich import print

class Product(BaseModel):
    product_id: int = Field(..., gt=0)  # must be > 0
    title: str = Field(..., min_length=3, max_length=50)
    price: float = Field(..., gt=0)
    in_stock: bool = True
    description: str = Field(default="No description", max_length=100)

#! Casual Example
product = Product(product_id=1, title="Sofa", price=999.99)
print(product)


#! Error: Input should be greater than 0 [type=greater_than, input_value=0, input_type=int]
second_product = Product(product_id=0, title="Chair", price=10)


from pydantic import field_validator

#! Custom validation for any field
class ProductWithFieldValidation(BaseModel):
    title: str

    @field_validator("title")
    def must_be_capitalized(cls, value):
        if not value[0].isupper():
            raise ValueError("Title must start with a capital letter")
        return value

third_product=ProductWithFieldValidation(title="Chair")
print(third_product)




from pydantic import model_validator

#! Custom validation for all the attributes
class ProductWithModelValidation(BaseModel):
    price: float
    discount: float

    @model_validator(mode="after")
    def check_discount(cls, values):
        if values.discount > values.price:
            raise ValueError("Discount cannot be more than price")
        return values
    
    
    @model_validator(mode="before")
    def validate_input(cls, values: dict) -> dict:
        # dict me chhed-chhaad karo before model banta
        values["price"] = values["price"] + 10.0
        return values

    
fourth_product=ProductWithModelValidation(price=100.0, discount=20.0)
print(fourth_product)


