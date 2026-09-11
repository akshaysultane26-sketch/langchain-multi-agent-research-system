from pydantic import BaseModel

class DemoModel(BaseModel):
    name: str
    age: int

test_data = DemoModel(name="Bappy", age=25)
print("SUCCESS: Pydantic is working perfectly:", test_data.model_dump())
