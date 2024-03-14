from data_store import data_schemas
from utility.custom_logger import logger
from utility.sns_publisher import publish_mobile_sms
from fastapi import status, HTTPException
from app.user_login_regisration_workflows.user_related_db_operations import UserRelatedDbOperations
from app.user_login_regisration_workflows.token_generator import TokenGenerator
from app.dependencies import get_formatted_phone_number, get_random_six_digit_otp, get_password_hash
from utility.custom_logger import logger
from pydantic import BaseModel, ValidationError

from app import settings


class HashedOtp(BaseModel):
    hashed_otp: str
    is_active: bool


class LoginExistingUser:
    def __init__(self, current_user, db_operation, sns=None):
        self.current_user: data_schemas.FirstTimeUser = current_user
        self.db_operation: UserRelatedDbOperations = db_operation
        self.sns = sns

    async def _get_user_data(self):
        return await self.db_operation.get_user(self.current_user)

    async def _update_user(self, data_to_update):
        return await self.db_operation.update_user_data(self.current_user, data_to_update)

    async def get_and_update_otp_activate_exiting_user_from_db(self, random_six_digit_otp):
        try:
            user_in_db = await self._get_user_data()
            logger.info(f"Existing data for user ind db is {user_in_db}")
            update_otp_for_existing_user = dict(user_in_db)
            update_otp_for_existing_user.update({"hashed_otp": get_password_hash(random_six_digit_otp),
                                                 "is_active": True})
            logger.info(f"Updated Data for db is {update_otp_for_existing_user}")

        except HTTPException:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User data not found. Signup First")
        else:
            return update_otp_for_existing_user

    @staticmethod
    def check_username_email_data(user_data: dict):
        return user_data.get("username", False) and user_data.get("email", False)

    @staticmethod
    def check_vehicle_data(user_data):
        return len(user_data.get("vehicle_data", 0)) > 0

    async def update_user_otp_and_provide_final_result(self, user_with_updated_otp):
        parsed_data_for_hashed_otp = HashedOtp.parse_obj(user_with_updated_otp)
        logger.info(f"final otp data to update in user db is {parsed_data_for_hashed_otp}")
        update_response = await self._update_user(parsed_data_for_hashed_otp.dict())
        logger.info(f"update response from db is {update_response}")
        return {"status_code": status.HTTP_200_OK,
                "message": f"OTP sent to {self.current_user.phonenumber} successfully",
                "data": {"otp_sent": True, "username_email_data": self.check_username_email_data(user_with_updated_otp),
                         "vehicle_data": self.check_vehicle_data(user_with_updated_otp)}}

    async def login_existing_user_through_otp(self):
        try:
            formatted_phone_number = get_formatted_phone_number(self.current_user.phonenumber)
            random_six_digit_otp = get_random_six_digit_otp()
            user_with_updated_otp = await self.get_and_update_otp_activate_exiting_user_from_db(random_six_digit_otp)
            response = publish_mobile_sms(self.sns, current_user=self.current_user,
                                          phonenumber=formatted_phone_number,
                                          current_otp=random_six_digit_otp)
        except HTTPException:
            raise
        else:
            return await self.update_user_otp_and_provide_final_result(user_with_updated_otp)


class LoginSocialMediaUser(LoginExistingUser):
    def __init__(self, current_user, db_operation, access_toke_expiry_time, algorithm, secret_key):
        super().__init__(current_user, db_operation)
        self.access_token_expiry_time = access_toke_expiry_time
        self.algorithm = algorithm
        self.secret_key = secret_key

    async def login_existing_user_through_social(self):
        try:
            user_in_db = data_schemas.AllUserData.parse_obj(await self._get_user_data())
            logger.info(f"Got user with social id in database {user_in_db}")
        except HTTPException:
            raise
        except ValidationError:
            logger.exception("Unable to parse the data for existing social media user")
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Unable to process social media user")
        else:
            logger.info("Creating new token for the existing social media user")
            access_token = TokenGenerator.create_access_token(data={"sub": user_in_db.phonenumber
                                                                    }, secret_key=self.secret_key,
                                                              algorithm=self.algorithm,
                                                              expire_time=self.access_token_expiry_time)
            dict_user_data = user_in_db.dict()
            return {"status_code": status.HTTP_200_OK, "message": "User logged in successfully. Auth token sent",
                    "access_token": access_token,
                    "data": {"access_token": access_token, "user_data": dict_user_data,
                             "username_email_data": self.check_username_email_data(user_data=dict_user_data),
                             "vehicle_data": self.check_vehicle_data(user_data=dict_user_data)}}


class LogoutExistingUser:
    def __init__(self, current_user, db_operation):
        self.current_user: data_schemas.FirstTimeUser = current_user
        self.db_operation: UserRelatedDbOperations = db_operation

    async def _get_user_data(self):
        return await self.db_operation.get_user(self.current_user)

    async def logout_user(self):
        user_data_to_update = {"is_active": False}
        try:
            response = await self.db_operation.update_user_data(self.current_user, user_data_to_update)
        except HTTPException:
            raise
        else:
            return {"status_code": status.HTTP_200_OK, "message": "User logged out successfully.",
                    "data": {}}
