
# FastAPI
from fastapi import HTTPException, Body,Path, Query, APIRouter,Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
#Typing
from typing import List
# database
from config.database import Session
from models.movie import Movie as MovieModel
#Middlewares
from middlewares.jwt_bearer import JWTBearer
# Service
from service.movie import MovieService
# Schemas
from schemas.movie import Movie

movie_router = APIRouter()



@movie_router.get(
    path="/movies",
    tags=["movies"],
    status_code=200,
    dependencies=[Depends(JWTBearer())]
    )
def get_movies():
    db = Session()
    result= MovieService(db).get_movies()
    return JSONResponse(status_code=200,content=jsonable_encoder(result))


@movie_router.get(
    path="/movies/{id}",
    tags=["movies"],
    response_model=List[Movie],
    status_code=200,
    )
def get_movies(id:int=Path(...)) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        raise HTTPException(status_code=404, detail="Movie not found")
    return JSONResponse(status_code=200,content=jsonable_encoder(result)) 


@movie_router.get(
    path="/movies/",
    tags=["movies"],
    response_model=Movie,
    status_code=200,
)
def get_movies_by_category(category: str=Query(...), year: int=Query(...)) -> List[Movie]: 
    db = Session()
    result = MovieService(db).get_movie_by_category(category)
    if not result:
        raise HTTPException(status_code=404, detail="Movie not found")
    return JSONResponse(status_code=200,content=jsonable_encoder(result))


@movie_router.post(
    path="/movies",
    tags=["movies"],
    status_code=201,
)
def create_movies(
    movie: Movie = Body(...), 
    
):
    db = Session()
    MovieService(db).create_movie(movie)
    return HTTPException(status_code=204, detail="Movie was created")


@movie_router.delete(
    path="/movies/{id}",
    tags=["movies"],
    response_model = dict
)
def delete_movie(id:int = Path(...)) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        raise HTTPException(status_code=404, detail="Movie not found")
    MovieService(db).delete_movie(id)
    return JSONResponse(content={"message": "Movie has been deleted"}) 
    

@movie_router.put(
    path="/movies/{id}",
    tags=["movies"],
    response_model = dict
)
def update_movie(
    id: int = Path(...),
    movie: Movie = Body(...), 
) -> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        raise HTTPException(status_code=404, detail="Movie not found")

    MovieService(db).update_movie(id,movie)
    return JSONResponse(content={"message": "Movie has been updated"}) 
