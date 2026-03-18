from pydantic import BaseModel, ConfigDict

class OrderCreate(BaseModel):
    pass # In a real app, you might pass specific items. We'll build form cart.

class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: str

    model_config = ConfigDict(from_attributes=True)

class PaymentRequest(BaseModel):
    order_id: int
    success: bool
