from pydantic import BaseModel
from typing import Optional

class OrderCreate(BaseModel):
    pass # In a real app, you might pass specific items. We'll build form cart.

class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: str

    class Config:
        from_attributes = True

class PaymentRequest(BaseModel):
    order_id: int
    success: bool
