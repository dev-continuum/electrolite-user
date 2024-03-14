import json
from functools import lru_cache
from fastapi import FastAPI
from fastapi_sso.sso.google import GoogleSSO
from fastapi_sso.sso.facebook import FacebookSSO
import boto3
from config import Settings
from utility.custom_logger import init_logging
from utility.secret_manager import get_aws_secret


settings = Settings()


import boto3
import base64
from botocore.exceptions import ClientError


session = boto3.session.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

secret_aws_keys = get_aws_secret(session, "aws_sns")
secret_facebook_credentials = get_aws_secret(session, "facebook_auth")
secret_google_credentials = get_aws_secret(session, "google_auth")

def get_sns():
    return session.client("sns",
                        region_name="ap-south-1",
                        aws_access_key_id=secret_aws_keys["aws_access_key_id"],
                        aws_secret_access_key=secret_aws_keys["aws_secret_access_key"])


def get_db():
    return session.resource('dynamodb', region_name=settings.DYNAMODB_REGION)


def get_lambda():
    return session.client('lambda', region_name=settings.LAMBDA_REGION)


def get_s3():
    return boto3.client("s3")


def get_sqs():
    return session.client("sqs", region_name=settings.LAMBDA_REGION)


def get_step_function():
    return session.client("stepfunctions", region_name=settings.LAMBDA_REGION)


app = FastAPI()
init_logging()

google_sso = GoogleSSO(
    client_id=secret_google_credentials["GOOGLE_CLIENT_ID"],
    client_secret=secret_google_credentials["GOOGLE_CLIENT_SECRET"],
    redirect_uri=settings.GOOGLE_REDIRECT_URI,
    use_state=False,
)

facebook_sso = FacebookSSO(
    client_id=secret_facebook_credentials["FACEBOOK_CLIENT_ID"],
    client_secret=secret_facebook_credentials["FACEBOOK_CLIENT_SECRET"],
    redirect_uri=settings.FACEBOOK_REDIRECT_URI,
    use_state=False,
)


from data_store.database import create_tables

create_tables()

from .security_routers import security_router
from .station_routers import station_router

app.include_router(security_router.router)
app.include_router(station_router.router)
