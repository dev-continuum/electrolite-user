from data_store import data_schemas
from utility.custom_logger import logger
from boto3.exceptions import S3UploadFailedError
from app import settings
from fastapi import status, HTTPException
from app.user_login_regisration_workflows.user_related_db_operations import UserRelatedDbOperations


class ProfileOperations:
    def __init__(self, current_user, db_operations):
        self.current_user = current_user
        self.db_operations: UserRelatedDbOperations = db_operations
        self.s3_path = f'{self.current_user.phonenumber}/image.jpg'
        self.bucket_name = settings.S3_USER_PROFILE_BUCKET

    async def get_profile(self):
        try:
            current_user = await self.db_operations.get_user(self.current_user)
        except HTTPException:
            raise
        else:
            return {"status_code": status.HTTP_200_OK, "message": f"Here is the profile data for the user",
                    "data": data_schemas.AllUserData.parse_obj(current_user)}

    async def set_profile(self, profile_data_to_update):
        try:
            current_user = await self.db_operations.update_user_data(self.current_user, profile_data_to_update)
        except HTTPException:
            raise
        else:
            return {"status_code": status.HTTP_200_OK, "message": f"Here is the profile data for the user",
                    "data": profile_data_to_update.dict()}

    async def set_image(self, image_content, s3_client):
        try:
            put_response = s3_client.put_object(Body=image_content, Bucket=self.bucket_name, Key=self.s3_path,)
            profile_data_to_update = {"profile_pic": f"https://{self.bucket_name}.s3.{settings.DYNAMODB_REGION}.amazonaws.com/{self.s3_path}"}
            current_user = await self.db_operations.update_user_data(self.current_user, profile_data_to_update)
        except S3UploadFailedError:
            logger.exception(f"Image Upload failed for user {self.current_user.phonenumber}")
            raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED, detail="Image upload failed")
        except HTTPException:
            raise
        else:
            return {"status_code": status.HTTP_200_OK, "message": f"Here is the profile data for the user",
                    "data": profile_data_to_update}

