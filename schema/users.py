from pydantic import BaseModel, EmailStr


class CreateUserSchema(BaseModel):
    email: EmailStr
    password: str


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str


class AdminUserSchema(BaseModel):
    email: EmailStr
    password: str


class CreateTaskSchema(BaseModel):
    title: str
    description: str
    assigned_to: EmailStr


class UpdateTaskSchema(BaseModel):
    title: str
    description: str
    assigned_to: EmailStr
    status: str
