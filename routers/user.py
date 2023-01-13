
# FastAPI
from fastapi import APIRouter
from fastapi.responses import JSONResponse
# jwt
from utils.jwt_manager import create_token
# Schemas
from schemas.user import User


user_router = APIRouter()


@user_router.post(
    path="/login",
    tags=["auth"]    
)
def login(user: User):
    if user.email =="admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200,content=token)
    return JSONResponse(status_code=403,content={"message":"User or password incorrect"})


