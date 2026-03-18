from pydantic import BaseModel, ConfigDict, Field

class CartAdd(BaseModel):
    product_id: int
    quantity: int = Field(default=1, ge=1)

class CartResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int

    model_config = ConfigDict(from_attributes=True)

class CartItemUpdate(BaseModel):
    quantity: int = Field(..., ge=1)
