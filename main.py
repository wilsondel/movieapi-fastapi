
# FastAPI
from fastapi import FastAPI, HTTPException, Body,Path, Query, Request,Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer

# Pydantic
from pydantic import BaseModel, Field

#Typing
from typing import Optional, List

# jwt
from jwt_manager import create_token, validate_token

# database
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel

app = FastAPI()
app.title = "My Fast API application"
app.version = "0.0.1"


Base.metadata.create_all(bind=engine)


class JWTBearer(HTTPBearer):

    # access to the users request
    async def __call__(self,request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["email"] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Invalid credentials")

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
    return JSONResponse(status_code=200,content=movies)


@app.get(
    path="/movies/{id}",
    tags=["movies"],
    response_model=List[Movie],
    status_code=200,
    )
def get_movies(id:int=Path(...)) -> List[Movie]:
    for movie in movies:
        if movie["id"] == id:
            return JSONResponse(status_code=200,content=movie) 
    raise HTTPException(status_code=404, detail="Movie not found")


@app.get(
    path="/movies/",
    tags=["movies"],
    response_model=Movie,
    status_code=200,
)
def get_movies_by_category(category: str=Query(...), year: int=Query(...)) -> List[Movie]:
    for movie in movies:
        if (movie["category"] == category): return JSONResponse(status_code=200,content=movie)
    raise HTTPException(status_code=404, detail="Movie not found")


@app.post(
    path="/movies",
    tags=["movies"],
    status_code=201,
)
def create_movies(
    movie: Movie = Body(...), 
    
):
    movies.append(movie)
    return HTTPException(status_code=204, detail="Movie was created")


@app.delete(
    path="/movies/{id}",
    tags=["movies"],
    response_model = dict
)
def delete_movie(id:int = Path(...)) -> dict:
    for idx, movie in enumerate(movies):
        if movie["id"] == id:
            del movies[idx]
            return JSONResponse(content={"message": "Movie has been deleted"}) 
    raise HTTPException(status_code=404, detail="Movie not found")
    

@app.put(
    path="/movies/{id}",
    tags=["movies"],
    response_model = dict
)
def update_movie(
    id: int = Path(...),
    movie: Movie = Body(...), 
) -> dict:
    for idx, mov in enumerate(movies):
        if mov["id"] == id:
            mov["title"] = movie.title
            mov["overview"] = movie.overview
            mov["year"] = movie.year
            mov["rating"] = movie.rating
            mov["category"] = movie.category
            return JSONResponse(content={"message": "Movie has been updated"}) 
    raise HTTPException(status_code=404, detail="Movie not found")
    