from pydantic import BaseSettings, AnyHttpUrl
from typing import Optional
import pathlib
import os

env_name = os.getenv("ACTIVE_ENVIRONMENT")
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")


class Settings(BaseSettings):
    WEBAPP: str
    PORT: int
    DYNAMODB: str
    DYNAMODB_REGION: str
    LAMBDA_REGION: str
    LOCAL_ENV: bool
    REDISHOST: Optional[str] = None
    REDISPORT: Optional[int] = None
    GOOGLE_REDIRECT_URI: AnyHttpUrl
    FACEBOOK_REDIRECT_URI: AnyHttpUrl
    AWS_ACCESS_KEY_ID: str = aws_access_key_id
    AWS_SECRET_ACCESS_KEY: str = aws_secret_access_key
    SEARCH_SERVICE_URL: AnyHttpUrl
    STEP_FUNCTION_ARN: str
    STEP_FUNCTION_FREQ_IN_SEC: int
    WEB_SOCKET_URL: str
    DB_API: AnyHttpUrl
    S3_USER_PROFILE_BUCKET: str


    class Config:
        env_file = pathlib.Path.joinpath(pathlib.Path(__file__).resolve().parents[0], f"config/{env_name}.env")


if __name__ == "__main__":
    settings = Settings()
