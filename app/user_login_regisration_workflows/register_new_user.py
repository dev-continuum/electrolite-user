from data_store import data_schemas
from utility.custom_logger import logger
from utility.sns_publisher import publish_mobile_sms
from fastapi import status, HTTPException
from app.user_login_regisration_workflows.user_related_db_operations import UserRelatedDbOperations
from app.dependencies import get_formatted_phone_number, get_random_six_digit_otp
from app.user_login_regisration_workflows.token_generator import TokenGenerator


class RegisterUser:
    def __init__(self, current_user, db_operation, sns=None):
        self.current_user: data_schemas.FirstTimeUser = current_user
        self.db_operation: UserRelatedDbOperations = db_operation
        self.sns = sns

    def check_if_this_user_exists(self):
        try:
            user_exist = self.db_operation.get_user(self.current_user)
        except HTTPException as e:
            if e.status_code == status.HTTP_404_NOT_FOUND:
                logger.info("User is new. Going ahead with new user registration")
            else:
                raise
        else:
            logger.info(f"{self.current_user} is re registering")
            # raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User is already registered. Login to proceed")

    async def otp_for_first_time_user(self):
        if not self.current_user.agree_terms:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Accept terms and conditions for first time user")
        else:
            self.check_if_this_user_exists()
            return await self.build_response_for_new_user()

    async def build_response_for_new_user(self):
        try:
            formatted_phone_number = get_formatted_phone_number(self.current_user.phonenumber)
            random_six_digit_otp = get_random_six_digit_otp()
            response = publish_mobile_sms(self.sns, current_user=self.current_user,
                                          phonenumber=formatted_phone_number,
                                          current_otp=random_six_digit_otp)
        except HTTPException:
            raise
        else:
            result = await self.create_user_and_return_final_response(random_six_digit_otp)
            username_email_data = False
            vehicle_data = False
            return {"status_code": status.HTTP_200_OK,
                    "message": f"OTP sent to {self.current_user.phonenumber} successfully",
                    "data": {"otp_sent": True, "username_email_data": username_email_data,
                             "vehicle_data": vehicle_data}}

    async def create_user_and_return_final_response(self, otp):
        try:
            result = await self.db_operation.create_new_user_in_database(self.current_user, otp)
        except HTTPException:
            raise
        else:
            return result


class RegisterSocialUser(RegisterUser):
    def __init__(self, current_user, db_operation, access_toke_expiry_time, algorithm, secret_key):
        super().__init__(current_user, db_operation)
        self.access_token_expiry_time = access_toke_expiry_time
        self.algorithm = algorithm
        self.secret_key = secret_key

    async def create_new_social_user(self):
        new_social_media_user = await self.create_user_and_return_final_response(otp="")
        logger.info(f"Registered an new social media user {new_social_media_user}")
        username_email_data = False
        vehicle_data = False
        access_token = TokenGenerator.create_access_token(data={"sub": self.current_user.phonenumber
                                                                }, secret_key=self.secret_key,
                                                          algorithm=self.algorithm,
                                                          expire_time=self.access_token_expiry_time)
        return {"status_code": status.HTTP_200_OK, "message": "User logged in successfully. Auth token sent",
                "access_token": access_token,
                "data": {"access_token": access_token,
                         "user_data": data_schemas.AllUserData.parse_obj(self.current_user).dict(),
                         "username_email_data": username_email_data, "vehicle_data": vehicle_data}}




