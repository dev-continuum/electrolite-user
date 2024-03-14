from data_store import data_schemas, crud_data_schemas, data_structures
from pydantic import ValidationError
from utility.custom_logger import logger
from fastapi import status, HTTPException
from data_store import crud
from app import settings
from app.dependencies import get_password_hash


class UserRelatedDbOperations:
    def __init__(self, db):
        self.db = db
        self.db_api = settings.DB_API

    async def create_new_user_in_database(self, current_user, current_otp):
        try:
            logger.info(f"Adding new user {current_user.phonenumber} to the db")
            final_user_data_to_create = current_user.dict()
            final_user_data_to_create.update({"hashed_otp": get_password_hash(current_otp),
                                              "is_active": True})
            new_user_entry = data_schemas.InitUser.parse_obj(final_user_data_to_create)
            new_user = await crud.create_entry_in_table(crud_data_schemas.CreateEntrySchema.parse_obj({
                "table_name": "User",
                "row_data": new_user_entry.dict()
            }))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Unable to update database")
        else:
            return new_user

    async def get_user(self, user):
        try:
            user_in_db = await crud.read_data_from_table(
                crud_data_schemas.ReadTableSchema.parse_obj({"table_name": "User",
                                                             "primary_key": "phonenumber",
                                                             "primary_key_value": user.phonenumber}))
        except HTTPException:
            raise
        else:
            try:
                return data_schemas.InitUser.parse_obj(user_in_db)
            except ValidationError:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    async def update_user_data(self, user, data_to_update):
        try:
            updated_user = await crud.update_table(crud_data_schemas.UpdateTableSchema.parse_obj({"table_name": "User",
                                                                                                  "primary_key": {
                                                                                                      "phonenumber": user.phonenumber},
                                                                                                  "data_to_update": data_to_update
                                                                                                  }))
        except HTTPException:
            raise
        else:
            return updated_user

    async def get_user_transactions(self, user) -> []:
        try:
            user_booking_history = await crud.read_data_from_table(
                crud_data_schemas.ReadTableSchema.parse_obj({"table_name": "ChargingSessionRecords",
                                                             "primary_key": "user_id",
                                                             "primary_key_value": user.phonenumber,
                                                             "index_name": 'user_id-booking_id-index',
                                                             "all_results": True}))
        except HTTPException:
            raise
        else:
            return user_booking_history

    async def get_user_booked_transactions(self, user) -> []:
        try:
            user_booking_history = await crud.read_data_from_table(
                crud_data_schemas.ReadTableSchema.parse_obj({"table_name": "ChargingSessionRecords",
                                                             "primary_key": "user_id",
                                                             "primary_key_value": user.phonenumber,
                                                             "sort_key": "current_status" ,
                                                             "sort_key_value": data_structures.ChargerStatus.CHARGER_BOOKED.value,
                                                             "index_name": 'user_id-current_status-index',
                                                             "all_results": True}))
        except HTTPException:
            raise
        else:
            return user_booking_history

    async def update_booking_table(self, booking_id, vendor_id, data_to_update):
        try:
            updated_user = await crud.update_table(crud_data_schemas.UpdateTableSchema.parse_obj({"table_name": "ChargingSessionRecords",
                                                                                                  "primary_key": {
                                                                                                      "booking_id": booking_id},
                                                                                                  "sort_key": {"vendor_id": vendor_id},
                                                                                                  "data_to_update": data_to_update
                                                                                                  }))
        except HTTPException:
            raise
        else:
            return updated_user