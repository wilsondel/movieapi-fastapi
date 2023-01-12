
# FastAPI
from fastapi import FastAPI, HTTPException, Body,Path, Query, Request,Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder

# Pydantic
from pydantic import BaseModel, Field

#Typing
from typing import Optional, List

# jwt
from jwt_manager import create_token, validate_token

# database
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel


#Middlewares
from middlewares.error_handler import ErrorHandler
from middlewares.jwt_bearer import JWTBearer

app = FastAPI()
app.title = "My Fast API application"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)

Base.metadata.create_all(bind=engine)


class User(BaseModel):
    email: str = Field(...)
    password: str = Field(...)


class Movie(BaseModel):
    id: Optional[int] = Field(default=None)
    title: str = Field(..., example="Dune", min_length=3,max_length=30)
    overview: str = Field(..., example="Great political and philosofical movie", min_length=15,max_length=50)
    year: int = Field(..., example="2020", le=2022, gt=1900)
    rating: float = Field(..., example="7.8", le=10, ge=0)
    category: str = Field(..., example="Action")

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


@app.get(
    path="/movies",
    tags=["movies"],
    status_code=200,
    dependencies=[Depends(JWTBearer())]
    )
def get_movies():
    db = Session()
    result=db.query(MovieModel).all()
    return JSONResponse(status_code=200,content=jsonable_encoder(result))


@app.get(
    path="/movies/{id}",
    tags=["movies"],
    response_model=List[Movie],
    status_code=200,
    )
def get_movies(id:int=Path(...)) -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Movie not found")
    return JSONResponse(status_code=200,content=jsonable_encoder(result)) 


@app.get(
    path="/movies/",
    tags=["movies"],
    response_model=Movie,
    status_code=200,
)
def get_movies_by_category(category: str=Query(...), year: int=Query(...)) -> List[Movie]: 
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category == category).all()
    if not result:
        raise HTTPException(status_code=404, detail="Movie not found")
    return JSONResponse(status_code=200,content=jsonable_encoder(result))


@app.post(
    path="/movies",
    tags=["movies"],
    status_code=201,
)
def create_movies(
    movie: Movie = Body(...), 
    
):
    db = Session()
    new_movie=MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return HTTPException(status_code=204, detail="Movie was created")


@app.delete(
    path="/movies/{id}",
    tags=["movies"],
    response_model = dict
)
def delete_movie(id:int = Path(...)) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Movie not found")
    db.delete(result)
    db.commit()
    return JSONResponse(content={"message": "Movie has been deleted"}) 
    

@app.put(
    path="/movies/{id}",
    tags=["movies"],
    response_model = dict
)
def update_movie(
    id: int = Path(...),
    movie: Movie = Body(...), 
) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id ==id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Movie not found")

    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category
    db.commit()
    return JSONResponse(content={"message": "Movie has been updated"}) 
