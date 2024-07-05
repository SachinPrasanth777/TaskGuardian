from fastapi import APIRouter, HTTPException
from utilities.database import Database
from schema.users import CreateUserSchema, LoginSchema
from utilities.response import JSONResponse
from utilities.bcrypt import hash_password, check_password

db = Database()
router = APIRouter()


@router.post("/signup")
async def handleSignUp(user: CreateUserSchema):
    email = db.users.find_one({"email": user.email})
    if email:
        raise HTTPException(status_code=400,detail="User Already Exists")
    hashed_password = hash_password(user.password).decode()
    db.users.insert_one({"email": user.email, "password": hashed_password})
    return JSONResponse({"success": True, "message": "User Signed Up Successfully"})

@router.post("/login")
async def handleLogin(user: LoginSchema):
    email = db.users.find_one({"email": user.email})
    if not email:
        raise HTTPException(status_code=404,detail="User does not Exist")
    value=check_password(user.password,email["password"])
    if not value:
        raise HTTPException(status_code=401,detail="Unauthorized Access/ Mismatched Passwords")
    return JSONResponse({"success":True,"message":"User Logged in Successfully"})
