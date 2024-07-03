from fastapi import APIRouter
from utilities.database import Database
from schema.users import CreateUserSchema
from utilities.response import JSONResponse
from utilities.bcrypt import get_password_hash

db=Database()
router=APIRouter()

@router.post('/signup')
async def handleSignUp(user: CreateUserSchema):
    email=db.users.find_one({"email":user.email})
    if(email):
        return JSONResponse({"success":False,"message":"User already Exists"})
    get_password_hash(user.password)
    return JSONResponse({"success":True,"message":"User Signed Up Successfully"})
    