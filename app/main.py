from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time
from . import models
from .database import engine
from .routers import auth, user, post, vote


# The following command is responsible for connecting with DB and making 
# necessary updates as we update the table schema (models.py). However,
# the autogenerate feature of alembic will automatically generate code to 
# implement those changes, so this can be commented out

# models.Base.metadata.create_all(bind=engine) 

origins = [
    "*"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}