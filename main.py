from fastapi import FastAPI
from routes.users import router
from utilities.response import JSONResponse

app=FastAPI()
app.include_router(router)

@app.get("/")
async def index():
    return JSONResponse({"success":True,"message":"All Modules loaded successfully"})