from vendor_workflow.common_workflows.all_common_utils import VendorCommunicationData
from pydantic import ValidationError
from fastapi import HTTPException, status
from vendor_workflow.electrolite_specific_workflow.electrolite_validation_classes import ElectroliteStartChargeParams, \
    ElectroliteHeaderChargeParams, ElectroliteStatusChargeParams, ElectroliteStopChargeParams
from utility.custom_logger import logger
from data_store.data_schemas import BookChargingSessionData


async def modify_response_data_as_per_electrolite(parsed_data_to_store_in_db: BookChargingSessionData,
                                                             data_for_user):
    try:
        ElectroliteStartChargeParams.parse_obj(data_for_user)
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Electrolite start charge params missing")
    else:
        logger.info(f"booking response details verified for electrolite. Returning to user {data_for_user}")
        return data_for_user


async def generate_electrolite_header_data(vendor_data: dict):
    """Put header related modifications here for the electrolite.
    Save the static header data in vendor db and modify it if needed here"""
    logger.info(f"vendor data after header modification is {vendor_data}")
    return vendor_data


async def generate_start_electrolite_body_data(charging_data, vendor_data: dict):
    """Put body related modifications here for the electrolite.
    Save the static header data in vendor db and modify it if needed here"""
    logger.info(f"vendor data after body modification is {vendor_data}")
    return vendor_data

async def generate_stop_electrolite_body_data(stop_charging_data, vendor_data):
    return vendor_data

async def generate_status_electrolite_body_data(status_charging_data, vendor_data):
    return vendor_data