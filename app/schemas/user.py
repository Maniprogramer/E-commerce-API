from pydantic import BaseModel, ConfigDict, Field

class UserCreate(BaseModel):
    email: str
    password: str = Field(..., min_length=6)

class UserResponse(BaseModel):
    id: int
    email: str
    is_admin: bool = False

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
