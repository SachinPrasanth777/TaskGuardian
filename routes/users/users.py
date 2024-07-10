from fastapi import APIRouter, HTTPException, Depends
from utilities.database import Database
from schema.users import CreateUserSchema, LoginSchema, VerifyOTPRequest
from utilities.response import JSONResponse
from utilities.bcrypt import hash_password, check_password
from utilities.jwt import create_access_token
from middleware.authentication import get_current_user
from mailer.mail import schedule_mail
from utilities.otp import check_otp
import json

db = Database()
router = APIRouter()


@router.post("/signup")
async def handleSignUp(user: CreateUserSchema):
    email = db.users.find_one({"email": user.email})
    if email:
        raise HTTPException(status_code=400, detail="User Already Exists")
    hashed_password = hash_password(user.password).decode()
    db.users.insert_one({"email": user.email, "password": hashed_password})
    return JSONResponse({"success": True, "message": "User Signed Up Successfully"})


@router.post("/generate-otp")
async def handleLogin(user: LoginSchema):
    email = db.users.find_one({"email": user.email})
    if not email:
        raise HTTPException(status_code=404, detail="User does not Exist")
    value = check_password(user.password, email["password"])
    if not value:
        raise HTTPException(
            status_code=401, detail="Unauthorized Access/ Mismatched Passwords"
        )
    schedule_mail(user.email)
    return JSONResponse({"success": True, "message": "OTP sent Successfully"})


@router.post("/verify-otp")
async def verify_otp(data: VerifyOTPRequest):
    if not check_otp(data.email, data.otp):
        raise HTTPException(status_code=400, detail="OTP Verification Failed")
    access_token = create_access_token({"email": data.email}, secret=db.secret)
    return JSONResponse(
        {
            "success": True,
            "message": "User Logged in Successfully",
            "token": access_token,
        }
    )


@router.get("/user")
async def upload_details(user: dict = Depends(get_current_user)):
    return JSONResponse({"success": True, "message": "User Fetched", "user": user})


@router.get("/tasks")
async def get_tasks(user: dict = Depends(get_current_user)):
    task_list= db.tasks.find({"assigned_to": user["email"]})
    if not task_list:
        raise HTTPException(status_code=404, detail="No Tasks Found")
    tasks=[]
    for task in task_list:
        tasks.append(task)
    return JSONResponse(content=json.loads(json.dumps(tasks, default=str)),media_type="application/json")
