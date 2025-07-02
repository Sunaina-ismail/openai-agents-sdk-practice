from pydantic import TypeAdapter
from rich import print
# Define a TypeAdapter for a list of integers
adapter = TypeAdapter(list[int])

# Validate some input data
only_int_list=[25,7,2]
mix_data_type_list=["4", 24, 42.4]
validated_data = adapter.validate_python(only_int_list)

print(validated_data)  # Output: [1, 2, 3]

from pydantic import BaseModel

class UserInfo(BaseModel):
    username: str
    roll_no: int

adapter = TypeAdapter(UserInfo)
schema = adapter.json_schema()
print(schema)