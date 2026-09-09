from typing import Optional
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str = "user"  # 'user', 'organizer', 'admin'
    department: Optional[str] = ""

class UserCreate(BaseModel):
    name: Optional[str] = None
    fullName: Optional[str] = None
    email: EmailStr
    password: str
    role: Optional[str] = "user"
    department: Optional[str] = ""

    def get_name(self) -> str:
        return self.fullName or self.name or self.email.split("@")[0].capitalize()

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    role: Optional[str] = None

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class UserStatusUpdate(BaseModel):
    status: str  # 'Active' | 'Inactive'

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    department: Optional[str] = ""
    status: str

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
