from pydantic import BaseModel,EmailStr

class CreateUserSchema(BaseModel):
    email: EmailStr
    password: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class TokenData(BaseModel):
    email: EmailStr | None = None