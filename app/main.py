
from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import vote,post, user, auth
from fastapi.middleware.cors import CORSMiddleware
from .config import settings



# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]


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

# app.include_router(comment.router)

@app.get("/")
def root():
    return {"message": "FastAPI + SQLAlchemy ORM running 🚀"}