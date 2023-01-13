
# FastAPI
from fastapi import HTTPException, Body,Path, Query, APIRouter,Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
# Pydantic
from pydantic import BaseModel, Field
#Typing
from typing import Optional, List
# database
from config.database import Session
from models.movie import Movie as MovieModel
#Middlewares
from middlewares.error_handler import ErrorHandler
from middlewares.jwt_bearer import JWTBearer


movie_router = APIRouter()


class Movie(BaseModel):
    id: Optional[int] = Field(default=None)
    title: str = Field(..., example="Dune", min_length=3,max_length=30)
    overview: str = Field(..., example="Great political and philosofical movie", min_length=15,max_length=50)
    year: int = Field(..., example="2020", le=2022, gt=1900)
    rating: float = Field(..., example="7.8", le=10, ge=0)
    category: str = Field(..., example="Action")



@movie_router.get(
    path="/movies",
    tags=["movies"],
    status_code=200,
    dependencies=[Depends(JWTBearer())]
    )
def get_movies():
    db = Session()
    result=db.query(MovieModel).all()
    return JSONResponse(status_code=200,content=jsonable_encoder(result))


@movie_router.get(
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


@movie_router.get(
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


@movie_router.post(
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


@movie_router.delete(
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
