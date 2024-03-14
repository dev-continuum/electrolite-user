from data_store import data_schemas
from utility.custom_logger import logger
from fastapi import status, HTTPException
from app.user_login_regisration_workflows.user_related_db_operations import UserRelatedDbOperations


class UserBookingReservationOperations:
    def __init__(self, current_user, db_operations):
        self.current_user = current_user
        self.db_operations: UserRelatedDbOperations = db_operations

    async def get_transactions(self):
        try:
            user_transaction_list = await self.db_operations.get_user_transactions(self.current_user)
        except HTTPException:
            raise
        else:
            return {"status_code": status.HTTP_200_OK, "message": f"Here is the user booking history",
                    "data": {"total_energy_charged": 0, "total_carbon_saved": 0, "charging_history": user_transaction_list}}
