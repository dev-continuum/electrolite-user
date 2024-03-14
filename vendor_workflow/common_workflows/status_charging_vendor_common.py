from utility.custom_logger import logger
from vendor_workflow.data_decision_maker.user_data_decision_maker import UserDataDecisionMaker
from vendor_workflow.data_decision_maker.db_data_decision_maker import DbUpdateDecisionMaker
from vendor_workflow.common_workflows.all_common_utils import VendorCommunicationData
from fastapi import status, HTTPException
from data_store import data_schemas
from vendor_workflow.data_decision_maker.dynamic_calculators import calculate_current_emission_saved, \
    calculate_current_range, calculate_current_battery_status


async def calculate_live_stats_based_on_response(status_charging_data, server_response) -> {}:
    server_response.update(calculate_current_battery_status(response_data=server_response))
    server_response.update(calculate_current_range(response_data=server_response,
                                                   vehicle_details=status_charging_data["expanded_vehicle_data"]))
    server_response.update(calculate_current_emission_saved(response_data=server_response,
                                                            vehicle_details=status_charging_data[
                                                                "expanded_vehicle_data"]))
    logger.info(f"Data after all the dynamic calculation {server_response}")
    return server_response


async def send_request_for_charging_status(third_party_communicator, parsed_vendor_data: VendorCommunicationData) -> {}:

    logger.info(f"Sending request to charger server with {parsed_vendor_data}")
    try:
        response = await third_party_communicator(parsed_vendor_data.final_endpoint, body=parsed_vendor_data.body_data,
                                                  header=parsed_vendor_data.header_data)
    except HTTPException:
        return {"status_code": status.HTTP_200_OK, "message": "Here is the current status",
                "current_energy_consumed": 5,
                "meter_values": {"V": 1, "W": 1, "A": 1, "Wh": 1, "SoC": 50}}
    else:
        return {"status_code": status.HTTP_200_OK, "message": "Here is the current status",
                "current_energy_consumed": 5,
                "meter_values": {"V": 1, "W": 1, "A": 1, "Wh": 1, "SoC": 50}}


async def prepare_data_for_db_update_based_on_response(response, charging_status_data_update):
    decision_maker = DbUpdateDecisionMaker(response=response,
                                           charging_data_update_for_session=charging_status_data_update,
                                           action="status")
    status_data_to_update_db = decision_maker.decide()
    return status_data_to_update_db


async def update_booking_table_for_charging_status(data_communicator, start_charging_data_update_for_session):
    return data_communicator.update_booking_table(data_schemas.BookChargingSessionData.parse_obj(
        start_charging_data_update_for_session))


async def prepare_data_for_internal_user(response, data_returned_from_db):
    state_data_from_db = data_returned_from_db["Attributes"]["charging_states"]
    logger.info(f"Passing this data to parse for user {state_data_from_db}")
    user_data_decision_maker = UserDataDecisionMaker(response=response,
                                                     updated_session_db_data=state_data_from_db,
                                                     action="status")
    status_data_to_return = user_data_decision_maker.decide()
    return status_data_to_return

