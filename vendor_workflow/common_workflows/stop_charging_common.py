from utility.custom_logger import logger
from vendor_workflow.data_decision_maker.user_data_decision_maker import UserDataDecisionMaker
from vendor_workflow.data_decision_maker.db_data_decision_maker import DbUpdateDecisionMaker
from vendor_workflow.common_workflows.all_common_utils import VendorCommunicationData
from data_store import data_schemas
from fastapi.exceptions import HTTPException
from fastapi import status
from data_store.data_structures import ChargerStatus


async def send_request_to_stop_charging(third_party_communicator, parsed_vendor_data: VendorCommunicationData):
    logger.info(f"Sending request to charger server with {parsed_vendor_data}")
    try:
        response = await third_party_communicator(parsed_vendor_data.final_endpoint, body=parsed_vendor_data.body_data,
                                                  header=parsed_vendor_data.header_data)
    except HTTPException:
        response = {"status_code": status.HTTP_200_OK, "message": "charging stopped"}
        return response
    else:
        response = {"status_code": status.HTTP_200_OK, "message": "charging stopped"}
        return response


async def prepare_data_for_db_update_based_on_response(response, stop_charging_data_for_session_update):
    decision_maker = DbUpdateDecisionMaker(response=response,
                                           charging_data_update_for_session=stop_charging_data_for_session_update,
                                           action="stop")
    status_data_to_update_db = decision_maker.decide()
    return status_data_to_update_db


async def prepare_data_for_user(response, updated_session_db_data):
    user_data_decision_maker = UserDataDecisionMaker(response=response,
                                                     updated_session_db_data=updated_session_db_data,
                                                     action="stop")
    status_data_to_return = user_data_decision_maker.decide()
    return status_data_to_return


async def update_booking_table_for_charge_stop_status(db_communicator, stop_charging_data_update_for_session):
    db_communicator.update_booking_table(data_schemas.BookChargingSessionData.parse_obj(
        stop_charging_data_update_for_session))


async def mark_charger_free_in_location_table(db_communicator, vendor_id, user_sent_stop_charge_data):
    data_chunk_to_update_charger_status = data_schemas.ChargingPointDataForUpdate.parse_obj(
        {"station_id": user_sent_stop_charge_data["station_id"],
         "vendor_id": vendor_id,
         "charger_point_id": user_sent_stop_charge_data["charger_point_id"],
         "charger_point_status": ChargerStatus.CHARGER_AVAILABLE,
         "connector_point_id": user_sent_stop_charge_data["connector_point_id"],
         "connector_point_status": ChargerStatus.CHARGER_AVAILABLE})
    db_communicator.update_charger_status_in_agg_table(data_chunk_to_update_charger_status)
