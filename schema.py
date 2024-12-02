from pydantic import BaseModel

# 1 - Base
class ItemBase(BaseModel):
    title: str
    description: str
    price: int

# 2 - request
class ItemCreate(ItemBase):
    pass

# 3 - Response
class ItemResponse(ItemBase):
    id: int
    class Config:
        from_attributes = True
