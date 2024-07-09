from fastapi import APIRouter, Request
from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi.responses import JSONResponse
from utilities.database import Database
from mailer.mail import schedule_mail

db = Database()
auth_router = APIRouter()

secret_key = db.secret_key

oauth = OAuth()
oauth.register(
    name="google",
    server_metadata_url=db.server_metadata_url,
    client_id=db.client_id,
    client_secret=db.secret_key,
    client_kwargs={"scope": "openid profile email"},
)


@auth_router.get("/login")
async def login(request: Request):
    uri = request.url_for("auth")
    return await oauth.google.authorize_redirect(request, uri)


@auth_router.get("/auth")
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        return JSONResponse(content={"error": e.error})
    user = token.get("userinfo")
    if user:
        request.session["user"] = dict(user)
        db.auth.insert_one({"email": user["email"]})
        schedule_mail(user["email"])
        return JSONResponse({"success": True, "message": "OTP sent Successfully"})
