from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .router import posts,user,auth,votes
from .config import settings

models.Base.metadata.create_all(bind=engine)

origins=["https://www.google.com"]

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.options("/",tags=["Health"])
def root():
    return {"message": "system is up and running"}