from vendor_workflow.chargemod_specific_workflow.chargemod_validaion_classes import ChargeModHeader, \
    ChargeModStartChargeParams, ChargeModChargeActivityParams, ChargeModStopChargeParams
from utility.custom_logger import logger
from data_store.data_schemas import BookChargingSessionData
from pydantic import ValidationError
from fastapi import HTTPException, status


async def generate_chargemod_header_data(vendor_data):
    header_data = ChargeModHeader.parse_obj(vendor_data["header_data"]).dict()
    logger.info(f"Current header data for the chargemod is {header_data}")
    vendor_data["header"] = header_data
    return vendor_data


async def generate_chargemod_start_body_data(charging_data, vendor_data):
    body_data = ChargeModStartChargeParams.parse_obj(charging_data).dict(exclude_none=True)
    logger.info(f"Generated start charge body data for the chargemod is {body_data}")
    vendor_data["body_data"] = body_data
    return vendor_data


async def generate_chargemod_stop_body_data(charging_data, vendor_data):
    body_data = ChargeModStopChargeParams.parse_obj(charging_data).dict(exclude_none=True)
    logger.info(f"Generated start charge body data for the chargemod is {body_data}")
    vendor_data["body_data"] = body_data
    return vendor_data


async def generate_chargemod_status_body_data(charging_data, vendor_data):
    body_data = ChargeModChargeActivityParams.parse_obj({"id": charging_data["reference_transaction_id"]}).dict(
        exclude_none=True)
    logger.info(f"Generated status charge body data for the chargemod is {body_data}")
    vendor_data["body_data"] = body_data
    return vendor_data


async def modify_response_data_as_per_chargemod(parsed_data_to_store_in_db: BookChargingSessionData,
                                                data_for_user):
    logger.info(f"Generating chargemod specific start charge data. current data for user is {data_for_user}")
    try:
        chargemod_specific_data = ChargeModStartChargeParams.parse_obj(
            {"station_id": parsed_data_to_store_in_db.station_id,
             "reference_transaction_id": parsed_data_to_store_in_db.reference_transaction_id,
             "user_id": parsed_data_to_store_in_db.vendor_user_id,
             "relay_switch_number": parsed_data_to_store_in_db.relay_switch_number,
             "max_energy_consumption": 10}).dict(exclude_none=True)
    except ValidationError:
        logger.exception("Value is missing for chargemod start charging data")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Value missing for chargemod start charging data")
    else:
        data_for_user["start_charging_data"].update(chargemod_specific_data)
    return data_for_user
