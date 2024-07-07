from fastapi.requests import Request
from fastapi import HTTPException
from utilities.database import Database
from utilities.jwt import read_token

db = Database()


async def get_current_user(req: Request):
    auth_header = req.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=403, detail="No token provided")
    token = auth_header.split(" ")[1]
    try:
        token_data = read_token(token, secret=db.secret)
        return token_data
    except Exception:
        raise HTTPException(status_code=403, detail="Invalid token")
