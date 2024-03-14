from data_store import data_schemas
from datetime import timedelta
from datetime import datetime
from typing import Optional
from app.user_login_regisration_workflows.user_related_db_operations import UserRelatedDbOperations
from fastapi import HTTPException, status
from app.dependencies import verify_password
from utility.custom_logger import logger
from jose import JWTError, jwt
from utility.custom_logger import logger


class TokenGenerator:
    def __init__(self, user_token_data: data_schemas.UserToken, db_operation, access_toke_expiry_time, algorithm,
                 secret_key):
        self.user_token_data = user_token_data
        self.db_operation: UserRelatedDbOperations = db_operation
        self.access_token_expiry_time = access_toke_expiry_time
        self.algorithm = algorithm
        self.secret_key = secret_key

    async def get_user_from_db(self):
        try:
            user_in_db = await self.db_operation.get_user(self.user_token_data)
        except HTTPException:
            raise
        else:
            return user_in_db

    async def authenticate_user(self):
        logger.info(f"Going to authenticate user {self.user_token_data}")
        user_in_db = await self.get_user_from_db()
        if not verify_password(self.user_token_data.otp, user_in_db.hashed_otp):
            # TODO: Major remove this once otp is matured
            if self.user_token_data.otp == '123456':
                return data_schemas.AllUserData.parse_obj(user_in_db.dict())

            logger.info(f"user authentication failed for user {self.user_token_data.phonenumber}")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Verification Failed. Please Enter correct OTP")
        else:
            logger.info(f"user authenticated successfully for user {self.user_token_data.phonenumber}")
            return data_schemas.AllUserData.parse_obj(user_in_db.dict())

    async def generate_token(self):
        try:
            user = await self.authenticate_user()
        except HTTPException:
            raise
        else:
            logger.info(f"user authenticated with info {user}")
            final_user = self.prepare_token_and_return(user)
            return final_user

    def prepare_token_and_return(self, user):
        access_token = self.create_access_token(
            data={"sub": self.user_token_data.phonenumber},
            secret_key=self.secret_key,
            algorithm=self.algorithm,
            expire_time=self.access_token_expiry_time
        )
        return {"status_code": status.HTTP_200_OK, "message": "User logged in successfully. Auth token sent",
                "data": {"access_token": access_token, "token_type": "bearer", "user_profile_data": user.dict()}}

    @staticmethod
    def create_access_token(data: dict, secret_key, algorithm, expire_time=None):
        if expire_time:
            access_token_expires = timedelta(minutes=expire_time)
            expire = datetime.utcnow() + access_token_expires
        else:
            expire = datetime.utcnow() + timedelta(minutes=60)

        logger.debug("creating access token")
        to_encode = data.copy()
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
        return encoded_jwt

