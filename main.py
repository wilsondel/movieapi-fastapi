
# FastAPI
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# database
from config.database import engine, Base
#Middlewares
from middlewares.error_handler import ErrorHandler
#Router
from routers.movie import movie_router
from routers.user import user_router

app = FastAPI()
app.title = "My Fast API application"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)




@app.get(
    path="/",
    tags=["home"]
    )
def message():
    return HTMLResponse("<h1>Hello, World!</h1>")


