from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class SecretKeys(BaseSettings):
    AWS_REGION: str = ""
    RAW_VIDEO_PROCESSING_QUEUE: str = ""