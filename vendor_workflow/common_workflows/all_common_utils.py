from data_store.data_organizer import DataCommunicator
from utility.custom_logger import logger
from fastapi.exceptions import HTTPException
from fastapi import status
from pydantic import BaseModel, AnyHttpUrl
from typing import Dict, Optional


class VendorCommunicationData(BaseModel):
    final_endpoint: str
    header_data: Optional[Dict] = None
    body_data: Optional[Dict] = None
    other_params: Optional[Dict] = None
    relay_to_ocpi_server: bool


async def ocpi_db_data_parser(vendor_data: dict, identifier, version="1.0"):
    logger.info(f"current identifier for vendor data parsing is {vendor_data}, "
                f"identifier {identifier}, version {version}")
    for endpoint in vendor_data["module_urls"][version]["endpoints"]:
        if endpoint["identifier"] == identifier:
            final_endpoint = endpoint["url"]
            break
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Vendor data not found in the database")
    header_data = vendor_data["header_data"]
    body_data = vendor_data["body_data"]
    other_params = vendor_data["other_params"]
    is_ocpi = vendor_data["ocpi"]
    final_vendor_communication_data = VendorCommunicationData.parse_obj(
        {"final_endpoint": final_endpoint, "header_data": header_data,
         "body_data": body_data,
         "other_params": other_params, "relay_to_ocpi_server": is_ocpi})
    logger.info(f"final endpoint for this activity is {final_vendor_communication_data}")
    return final_vendor_communication_data


async def get_url_params_from_db(db_communicator: DataCommunicator) -> dict:
    """
    :param vendor_id:
    :param db_communicator:
    :return: vendor data from vendor db
    """
    logger.info("getting vendor details from vendor db")
    return db_communicator.get_vendor_details_from_vendor_db()


def prepare_input_data_for_current_function(input_data, input_keys, start_charge_process_map: dict) -> []:
    current_input_list = []
    if input_data:
        current_input_list.extend(input_data)
    if input_keys:
        for current_key in input_keys:
            current_input_list.append(start_charge_process_map[current_key])
    return current_input_list


def get_user_selected_vehicle_data(book_charger_data, all_vehicle_data):
    model, registration_number = book_charger_data.vehicle_used.split("_")
    for vehicle in all_vehicle_data:
        if registration_number == vehicle["registration_number"]:
            logger.debug(f"Current vehicle for the booking is {vehicle}")
            return vehicle
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This vehicle does not exist in registered vehicle list")
