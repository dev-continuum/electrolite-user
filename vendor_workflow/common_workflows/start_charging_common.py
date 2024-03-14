from utility.custom_logger import logger
from vendor_workflow.data_decision_maker.user_data_decision_maker import UserDataDecisionMaker
from vendor_workflow.data_decision_maker.db_data_decision_maker import DbUpdateDecisionMaker
from vendor_workflow.common_workflows.all_common_utils import VendorCommunicationData
from utility.time_calculator import get_current_date_time_format
from fastapi import status, HTTPException
from data_store import data_schemas
from data_store.data_organizer import DataCommunicator


async def get_booking_details(booking_id, db_communicator: DataCommunicator) -> dict:
    logger.info("Getting booking details")
    return db_communicator.get_booking_details(booking_id)


async def check_for_booking_id_usage(booking_data) -> bool:
    logger.info("Checking if booking id is already used")
    if booking_data["start_charging_status"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Start for this booking id is already"
                                                                            " attempted. Create a new booking")
    return True


async def send_request_to_start_charging(start_charge_data: dict,
                                            third_party_communicator, parsed_vendor_data: VendorCommunicationData,
                                         calling_method):
    logger.info(f"Sending request to charger server with {parsed_vendor_data}")
    logger.info(f"Calling method for this request is {calling_method}")

    try:
        response = await third_party_communicator(parsed_vendor_data.final_endpoint, body=parsed_vendor_data.body_data,
                                                  header=parsed_vendor_data.header_data, calling_method=calling_method)
    except HTTPException:
        response = {"status_code": status.HTTP_200_OK, "message": "charging started"}
        current_time = get_current_date_time_format()
        response.update({"start_time": current_time["datetime_string"]})
        return response
    else:
        response = {"status_code": status.HTTP_200_OK, "message": "charging started"}
        current_time = get_current_date_time_format()
        response.update({"start_time": current_time["datetime_string"]})
        return response


async def prepare_data_for_db_update_based_on_response(response, start_charging_data_update_for_session):
    logger.info("Preparing data for the db update")
    decision_maker = DbUpdateDecisionMaker(response=response,
                                           charging_data_update_for_session=start_charging_data_update_for_session,
                                           action="start")
    status_data_to_update_db = decision_maker.decide()
    return status_data_to_update_db


async def update_booking_table_for_charge_start_status(db_communicator: DataCommunicator,
                                                       start_charging_data_update_for_session):
    logger.info("Going to update booking table")
    db_communicator.update_booking_table(data_schemas.BookChargingSessionData.parse_obj(
        start_charging_data_update_for_session))


async def prepare_data_for_user(user_sent_start_charge_data, response, updated_session_db_data):
    logger.info("preparing final data for the user")
    user_sent_start_charge_data.update({"charging_activity_id": updated_session_db_data["charging_activity_id"]})
    user_data_decision_maker = UserDataDecisionMaker(response=response,
                                                     updated_session_db_data=updated_session_db_data,
                                                     charging_data=user_sent_start_charge_data,
                                                     action="start")
    status_data_to_return = user_data_decision_maker.decide()
    return status_data_to_return

# return to user
