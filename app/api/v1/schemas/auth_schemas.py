from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreateSchema(BaseModel):
    """Schema para criação de usuário."""
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserLoginSchema(BaseModel):
    """Schema para login."""
    username: str
    password: str


class UserResponseSchema(BaseModel):
    """Schema de resposta do usuário."""
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True


class TokenSchema(BaseModel):
    """Schema de resposta do token."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponseSchema

