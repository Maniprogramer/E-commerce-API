from pydantic import BaseModel
from typing import Optional

class CartAdd(BaseModel):
    product_id: int
    quantity: int = 1

class CartResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True

class CartItemUpdate(BaseModel):
    quantity: int
