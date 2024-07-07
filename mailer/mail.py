from fastapi import APIRouter
from utilities.response import JSONResponse
import certifi
import ssl
from utilities.otp import generate_otp
from pydantic import EmailStr
from email.message import EmailMessage
from utilities.database import Database
import smtplib

db = Database()
mail_router = APIRouter()


def schedule_mail(mail: EmailStr):
    try:
        em = EmailMessage()
        em["From"] = db.username
        em["To"] = mail
        em["Subject"] = "Please Verify Your OTP"
        em.set_content(f"Your OTP is {generate_otp(mail)}")
        context = ssl.create_default_context(cafile=certifi.where())
        with smtplib.SMTP_SSL("smtp.gmail.com", db.port, context=context) as smtp:
            smtp.login(db.username, db.password)
            smtp.sendmail(db.username, mail, em.as_string())
    except smtplib.SMTPException:
        return JSONResponse({"success": False, "message": "Failed to Send Email"})
