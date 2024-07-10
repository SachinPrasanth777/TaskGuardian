from fastapi import APIRouter, HTTPException, Depends
from pydantic import EmailStr
from utilities.response import JSONResponse
from utilities.database import Database
from utilities.bcrypt import hash_password, check_password
from schema.users import (
    AdminUserSchema,
    VerifyOTPRequest,
    CreateTaskSchema,
    UpdateTaskSchema,
)
from utilities.jwt import create_access_token
from mailer.mail import schedule_mail, schedule_mail_task
from utilities.otp import check_otp
from middleware.authentication import get_current_user

admin_router = APIRouter()
db = Database()


@admin_router.post("/signup")
async def handleSignUp(user: AdminUserSchema):
    email = db.admins.find_one({"email": user.email})
    if email:
        raise HTTPException(status_code=400, detail="Admin Already Exists")
    hashed_password = hash_password(user.password).decode()
    db.admins.insert_one({"email": user.email, "password": hashed_password})
    db.admins.find_one_and_update(
        {"email": user.email}, {"$set": {"isVerified": False}}
    )
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


@admin_router.post("/create-task")
async def create_task(
    task: CreateTaskSchema, current_user: dict = Depends(get_current_user)
):
    user = db.users.find_one({"email": task.assigned_to})
    if not user:
        raise HTTPException(status_code=404, detail="User does not Exist")
    schedule_mail_task(task.assigned_to)
    db.tasks.insert_one(
        {
            "title": task.title,
            "description": task.description,
            "assigned_to": task.assigned_to,
        }
    )
    db.tasks.find_one_and_update(
        {"title": task.title},
        {"$set": {"created_by": current_user["email"], "status": "Not Completed"}},
    )
    return JSONResponse({"success": True, "message": "Task Created Successfully"})


@admin_router.delete("/delete-task/{task_title}")
async def delete_task(task_title: str, current_user: dict = Depends(get_current_user)):
    task = db.tasks.find_one({"title": task_title})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.tasks.delete_one({"title": task_title})
    return JSONResponse(
        {
            "success": True,
            "message": f"Task {task_title} Deleted Successfully by {current_user['email']}",
        }
    )


@admin_router.put("/update-task/{task_title}")
async def update_task(
    task_title: str,
    task: UpdateTaskSchema,
    current_user: dict = Depends(get_current_user),
):
    task_record = db.tasks.find_one({"title": task_title})
    if not task_record:
        raise HTTPException(status_code=404, detail="Task not found")
    task_assignee = task_record["assigned_to"]
    update_data = {"title": task.title, "description": task.description}
    if task.assigned_to:
        user = db.users.find_one({"email": task.assigned_to})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if task_assignee != task.assigned_to:
            update_data["assigned_to"] = task.assigned_to
            schedule_mail_task(task.assigned_to)
    if task.title != task_record["title"]:
        update_data["title"] = task.title
    if task.description != task_record["description"]:
        update_data["description"] = task.description
    if task.status:
        update_data["status"] = task.status
    db.tasks.find_one_and_update({"title": task_title}, {"$set": update_data})
    return JSONResponse(
        {
            "success": True,
            "message": f"Task {task_title} Updated Successfully by {current_user['email']}",
        }
    )
