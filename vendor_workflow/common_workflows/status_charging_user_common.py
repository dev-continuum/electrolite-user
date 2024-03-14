from utility.custom_logger import logger
from data_store.data_organizer import DataCommunicator
from vendor_workflow.data_decision_maker.user_data_decision_maker import UserDataDecisionMaker
from vendor_workflow.data_decision_maker.db_data_decision_maker import DbUpdateDecisionMaker
from fastapi import status, HTTPException
from data_store import data_schemas
from data_store.data_structures import ChargingStatus


class UserStatusCharging:
    def __init__(self, vendor_id, booking_id, socket_connection_id, charging_status_data, db, sqs, data_communicator):
        self.status_charging_data = charging_status_data
        self.data_communicator: DataCommunicator = data_communicator(vendor_id, db, sqs)
        self.booking_id = booking_id
        self.vendor_id = vendor_id
        self.socket_connection_id = socket_connection_id

    async def update_and_read_current_status(self):
        if self.socket_connection_id:
            logger.debug("There is a new socket id preparing for db update")
            data_to_update = {"booking_id": self.booking_id, "vendor_id": self.vendor_id, "socket_connection_id": self.socket_connection_id}
            return self.update_booking_table_for_charging_status(data_to_update)["Attributes"]
        else:
            logger.debug("There is a no new socket. no update needed. Going to read data")
            return self.data_communicator.get_booking_details(self.booking_id)

    async def provide_user_charging_status(self):
        try:
            current_status = await self.update_and_read_current_status()
        except HTTPException:
            raise
        else:
            logger.debug(f"Data returned after db update is {current_status}")
            charging_status_data_for_user = self.prepare_data_for_end_user({"status_code": status.HTTP_200_OK},
                                                                           current_status["charging_states"])
            return charging_status_data_for_user

    def update_booking_table_for_charging_status(self, start_charging_data_update_for_session):
        return self.data_communicator.update_booking_table(data_schemas.BookChargingSessionData.parse_obj(
            start_charging_data_update_for_session))

    def prepare_data_for_end_user(self, response, current_session_db_data):
        logger.info(f"Passing this data to parse for user {current_session_db_data}")
        user_data_decision_maker = UserDataDecisionMaker(response=response,
                                                         updated_session_db_data=current_session_db_data,
                                                         action="status")
        status_data_to_return = user_data_decision_maker.decide()
        return status_data_to_return
