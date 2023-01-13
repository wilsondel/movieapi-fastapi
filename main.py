
# FastAPI
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
# Pydantic
from pydantic import BaseModel, Field
# jwt
from jwt_manager import create_token
# database
from config.database import engine, Base
#Middlewares
from middlewares.error_handler import ErrorHandler
#Router
from routers.movie import movie_router

app = FastAPI()
app.title = "My Fast API application"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)
app.include_router(movie_router)

Base.metadata.create_all(bind=engine)


class User(BaseModel):
    email: str = Field(...)
    password: str = Field(...)



movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    }, 
    {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    }, 
]

@app.get(
    path="/",
    tags=["home"]
    )
def message():
    return HTMLResponse("<h1>Hello, World!</h1>")



@app.post(
    path="/login",
    tags=["auth"]    
)
def login(user: User):
    if user.email =="admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200,content=token)
    return JSONResponse(status_code=403,content={"message":"User or password incorrect"})

