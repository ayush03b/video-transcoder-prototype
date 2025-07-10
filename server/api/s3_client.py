from api.deps import db_dependency
from fastapi import status, HTTPException, APIRouter, Query
from typing import List
import boto3
from core.config import settings
from uuid import uuid4

router = APIRouter()

s3_client = boto3.client(
    "s3",
    region_name=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)

@router.get("/generate-presigned-url")
def generate_presigned_url(file_name: str = Query(...), file_type: str = Query(...)):
    unique_key = f"videos/{uuid4()}_{file_name}"

    try:
        URL = s3_client.generate_presigned_url(
            ClientMethod="put_object",
            Params = {
                "Bucket" : settings.S3_BUCKET_NAME,
                "Key" : unique_key,
                "ContentType" : file_type,
            },
            ExpiresIn=300
        )
        return {"url" : URL, "key" : unique_key}
    except Exception as e:
        return {"error" : str(e)}
    