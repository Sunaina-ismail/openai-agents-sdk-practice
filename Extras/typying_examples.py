# ---------------------------------------
# ✅ Imports
# ---------------------------------------
from typing import (
    Optional,
    Literal,
    Callable,
    Any,
    TypeVar,
    Generic,
    List,
    Dict,
    Tuple,
    Set,
    Annotated,
    TypedDict,
    Union,
)
from pydantic import Field, BaseModel

# ---------------------------------------
# ✅ Basic Typing Examples
# ---------------------------------------

names: List[str] = ["Ali", "Ahmed"]
scores: Dict[str, int] = {"Ali": 90}
pair: Tuple[str, int] = ("Age", 25)
unique: Set[int] = {1, 2, 3}
data: Any = "can be anything"

# ---------------------------------------
# ✅ Optional Type Example
# ---------------------------------------

def get_age(user: str) -> Optional[int]:
    if len(user) % 2 == 0:
        return 10
    return None

# ---------------------------------------
# ✅ Basic Function Typing
# ---------------------------------------

def greet(name: str) -> str:
    return f"Hello {name}"

greet("Fasih")

# ---------------------------------------
# ✅ Union Type
# ---------------------------------------

def process(data: Union[str, int]):
    print(data)

# ---------------------------------------
# ✅ Literal Type
# ---------------------------------------

traffic_light: Literal["red", "green", "orange"] = "green"

# ---------------------------------------
# ✅ Callable Type
# ---------------------------------------

def run_operation(op: Callable[[int, int], int]):
    return op(2, 3)

def sum(a: int, b: int) -> int:
    return a + b

data = run_operation(sum)
print(data)

# ---------------------------------------
# ✅ TypeVar + Generic Function
# ---------------------------------------

T = TypeVar("T")  # T can be any type

def first_item(items: List[T]) -> T:
    return items[0]

print(first_item([1, 2, 3, 4, 5]))
print(first_item(["hello", "world"]))

# ---------------------------------------
# ✅ Generic Class
# ---------------------------------------

class Box(Generic[T]):
    def __init__(self, value: T):
        self.value = value

box = Box[str]("data")
print(box.value)

box_2 = Box 
print(box_2.value)

# ---------------------------------------
# ✅ Annotated + Pydantic Field
# ---------------------------------------

class User(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=10)]

user = User(name="a")

# ---------------------------------------
# ✅ TypedDict
# ---------------------------------------

class UserDict(TypedDict):
    name: str
    age: int

user_dict: UserDict = {"name": "Ali", "age": 22}
print(user_dict)

# ---------------------------------------
# ✅ Typing Quick Reference Table (Markdown)
# ---------------------------------------

"""
| Feature       | Use                                 |
| ------------- | ----------------------------------- |
| `List[str]`   | List of strings                     |
| `Optional[X]` | X ya None                           |
| `Union[X, Y]` | X ya Y dono valid                   |
| `Literal[]`   | Sirf specified value allowed        |
| `Callable`    | Function type                       |
| `TypeVar`     | Generic/Template type               |
| `Generic[T]`  | Class generic banane ke liye        |
| `Annotated`   | Metadata + type hints (Pydantic v2) |
| `TypedDict`   | Strict schema wali dictionary       |
"""
