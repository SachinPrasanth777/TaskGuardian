from fastapi import FastAPI
from routes.users import router
from routes.auth import auth_router
from utilities.response import JSONResponse
from utilities.database import Database
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware

db = Database()
app = FastAPI()

secret_key = db.secret_key
app.add_middleware(SessionMiddleware, secret_key=secret_key)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
app.include_router(auth_router)


@app.get("/")
async def index():
    return JSONResponse({"success": True, "message": "All Modules loaded successfully"})
