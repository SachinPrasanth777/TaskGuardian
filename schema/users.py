from pydantic import BaseModel,EmailStr

class CreateUserSchema(BaseModel):
    email: EmailStr
    password: str