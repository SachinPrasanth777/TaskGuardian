from fastapi import APIRouter
from utilities.database import Database
from schema.users import CreateUserSchema
from utilities.response import JSONResponse
from utilities.bcrypt import hash_password

db = Database()
router = APIRouter()


@router.post("/signup")
async def handleSignUp(user: CreateUserSchema):
    email = db.users.find_one({"email": user.email})
    if email:
        return JSONResponse({"success": False, "message": "User already Exists"})
    hashed_password = hash_password(user.password).decode()
    db.users.insert_one({"email": user.email, "password": hashed_password})
    return JSONResponse({"success": True, "message": "User Signed Up Successfully"})
