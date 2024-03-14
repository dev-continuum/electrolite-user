from app.user_login_regisration_workflows.user_related_db_operations import UserRelatedDbOperations
from utility.custom_logger import logger
from data_store import data_schemas, data_structures

class CheckUserBookings:
    def __init__(self, db, current_user, book_charger_data: data_schemas.BookChargerData):
        self.user_related_db_operations = UserRelatedDbOperations(db)
        self.user = current_user
        self.book_charger_data = book_charger_data

    async def check_booking_for_current_user(self):
        current_user_transactions = await self.user_related_db_operations.get_user_booked_transactions(self.user)
        logger.debug(f"List of current user bookings are {current_user_transactions}")
        for booking in current_user_transactions:
            if booking["charger_point_id"] == self.book_charger_data.charger_point_id and booking["connector_point_id"] == self.book_charger_data.connector_point_id:
                # We have to mark current state machine to reconize this state. Machine should
                logger.info("Marking this booking as rebooked so that current state machine will stop")
                await self.user_related_db_operations.update_booking_table(booking_id=booking["booking_id"],vendor_id=booking["vendor_id"],
                                                                           data_to_update=
                                                                    {"current_status": data_structures.ChargingStatus.REBOOKED.name})
                logger.info(f"Charger {self.book_charger_data.charger_point_id} is booked by same user hence going ahead with rebooking")
                return True
        else:
            return False



