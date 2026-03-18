from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class ProductBase(BaseModel):
    name: str
    price: float = Field(..., gt=0)
    category: str

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0)
    category: Optional[str] = None

class ProductResponse(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
