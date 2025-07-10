from fastapi import FastAPI
from db_setup import engine
import models
from api import api_router
from core.config import settings
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(
    bind=engine
)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,         
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/server")


@app.get("/")
def root():
    return {"data": "API working!"}