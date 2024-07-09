from fastapi import APIRouter,HTTPException
from utilities.response import JSONResponse
from utilities.database import Database
from utilities.bcrypt import hash_password, check_password
from schema.users import AdminUserSchema,VerifyOTPRequest
from utilities.jwt import create_access_token
from mailer.mail import schedule_mail
from utilities.otp import check_otp

admin_router=APIRouter()
db=Database()

@admin_router.post("/signup")
async def handleSignUp(user: AdminUserSchema):
    email = db.admins.find_one({"email": user.email})
    if email:
        raise HTTPException(status_code=400, detail="Admin Already Exists")
    hashed_password = hash_password(user.password).decode()
    db.admins.insert_one({"email": user.email, "password": hashed_password})
    db.admins.find_one_and_update({"email":user.email},{"$set":{"isVerified":False}})
    return JSONResponse({"success": True, "message": "Admin Signed Up Successfully"})

@admin_router.post("/generate-otp")
async def handleLogin(user: AdminUserSchema):
    email = db.admins.find_one({"email": user.email})
    if not email:
        raise HTTPException(status_code=404, detail="Admin does not Exist")
    value = check_password(user.password, email["password"])
    if not value:
        raise HTTPException(
            status_code=401, detail="Unauthorized Access/ Mismatched Passwords"
        )
    if not email["isVerified"]:
        raise HTTPException(status_code=401, detail="Admin is not Verified")
    schedule_mail(user.email)
    return JSONResponse({"success": True, "message": "OTP sent Successfully"})

@admin_router.post("/verify-otp")
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
