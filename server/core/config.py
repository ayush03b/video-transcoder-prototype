from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "ByteCry"
    VERSION: str = "1.0"
    AWS_REGION: str = ""
    S3_BUCKET_NAME: str = ""
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    POSTGRES_DB_URL: str = ""
    class Config:
        env_file = ".env"


settings = Settings()