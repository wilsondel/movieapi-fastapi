
# Pydantic
from pydantic import BaseModel, Field
#Typing
from typing import Optional

class Movie(BaseModel):
    id: Optional[int] = Field(default=None)
    title: str = Field(..., example="Dune", min_length=3,max_length=30)
    overview: str = Field(..., example="Great political and philosofical movie", min_length=15,max_length=50)
    year: int = Field(..., example="2020", le=2022, gt=1900)
    rating: float = Field(..., example="7.8", le=10, ge=0)
    category: str = Field(..., example="Action")

