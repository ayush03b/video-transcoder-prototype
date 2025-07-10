from fastapi import APIRouter
from . import s3_client

api_router = APIRouter()
api_router.include_router(s3_client.router)