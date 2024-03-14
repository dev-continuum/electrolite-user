from data_store import data_schemas
from data_store.data_structures import ChargerStatus, ChargingCalculationMode, ChargingStatus
from tariff_calculation.tariff_calculator import Tariff
from utility.custom_logger import logger
from fastapi import HTTPException, status
import uuid


async def check_charger_status(available_chargers, book_charger_data) -> dict:
    is_available = False
    is_bookable = False
    one_charger_data = None
    for charger in available_chargers:
        one_charger_data = charger
        if charger["charger_point_id"] == book_charger_data.charger_point_id:
            for connector in charger["connectors"]:
                if connector["connector_point_id"] == book_charger_data.connector_point_id:
                    is_available = True
                    if charger["charger_point_status"] == ChargerStatus.CHARGER_AVAILABLE.value \
                            and connector["status"] == ChargerStatus.CHARGER_AVAILABLE.value:
                        is_bookable = True
                        break
    return {"is_available": is_available, "is_bookable": is_bookable, "one_charger_data": one_charger_data}


async def strategy_decision(check_user_bookings, charger_status: dict) -> bool:
    if charger_status["is_available"] and charger_status["is_bookable"] and charger_status["one_charger_data"]:
        return True
    elif charger_status["is_available"] and not charger_status["is_bookable"]:
        proceed_with_booking = await check_user_bookings.check_booking_for_current_user()
        if proceed_with_booking:
            return True
        else:
            raise HTTPException(
                status_code=status.HTTP_412_PRECONDITION_FAILED,
                detail="This charger point exists but not available at the moment")

    elif not charger_status["is_available"]:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail="Please check the if charger point provided is correct")
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unknown error please check charger point id, connector id and other details")


async def get_tariff_object(book_charger_data, vendor_data):
    # self.tariff_data = get_data_from_s3_bucket(s3_client, bucket_name="electrolite-vendor-data",
    #                                            file_name="tariff_rates.json")
    logger.info(f"Generating traffic object for {book_charger_data.vendor_id}")
    logger.info(f"Providing tariff data {vendor_data['tariff_data']}")
    return Tariff(book_charger_data.vendor_id, vendor_data["tariff_data"])


async def prepare_static_data_for_db_update(book_charger_data, current_vehicle_data_for_booking):
    static_data_to_update_db = book_charger_data.dict()
    static_data_to_update_db["expanded_vehicle_data"] = current_vehicle_data_for_booking
    return static_data_to_update_db


async def get_current_charger_power_capacity(book_charger_data, available_chargers):
    for charger in available_chargers:
        if charger["charger_point_id"] == book_charger_data.charger_point_id:
            if "vac" in charger["power_capacity"].lower():
                voltage_current_list = charger["power_capacity"].split(",")
                voltage_value = int(''.join(filter(str.isdigit, voltage_current_list[0].strip())))
                current_value = int(''.join(filter(str.isdigit, voltage_current_list[1].strip())))
                power_in_kw = (voltage_value * current_value) / 1000
                logger.debug(f"power was provided in VAC A. Converted power for station is {power_in_kw}")
                return power_in_kw
            elif "kw" in charger["power_capacity"].lower():
                power_in_kw = int(''.join(filter(str.isdigit, charger["power_capacity"])))
                logger.debug(f"power was provided in KW. Formatted power for station is {power_in_kw}")
                return power_in_kw


async def get_estimated_tariff(book_charger_data, current_vehicle_data_for_booking,
                               current_power_capacity, tariff_object):
    if book_charger_data.calculation_method == ChargingCalculationMode.TIME_BASED_CALCULATION:
        return tariff_object.calculate_estimated_tariff(
            duration_time_stamp=book_charger_data.target_duration_timestamp,
            target_vehicle_data=current_vehicle_data_for_booking,
            target_station_power_in_kw=current_power_capacity)
    elif book_charger_data.calculation_method == ChargingCalculationMode.ENERGY_BASED_CALCULATION:
        return tariff_object.calculate_estimated_tariff(
            energy_needed_in_kw=book_charger_data.target_energy_kw,
            target_vehicle_data=current_vehicle_data_for_booking,
            target_station_power_in_kw=current_power_capacity)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="One charging mode must be selected either TIME or ENERGY")


async def get_current_wallet_recharge_details(wallet_balance, estimated_tariff_data):
    final_estimated_cost = estimated_tariff_data["amount_after_gst"]
    logger.info(f"Current wallet balance for user is {wallet_balance} and estimated cost is {final_estimated_cost}")
    if wallet_balance >= final_estimated_cost:
        return {"recharge_required": False, "difference_amount": None}
    else:
        return {"recharge_required": True, "difference_amount": str(final_estimated_cost - wallet_balance)}


async def generate_and_update_dynamic_data_for_session(current_time_related_data, one_station_data,
                                                       charger_status_data, static_data_to_update_db,
                                                       estimated_tariff_data, wallet_recharge_data, tariff_object,
                                                       relay_switch_number=None, reference_transaction_id=None,
                                                       vendor_user_id=None):
    final_data_for_db_update = static_data_to_update_db.copy()
    one_charger_data = charger_status_data["one_charger_data"]
    current_dynamic_data = {"booking_id": str(uuid.uuid4()),
                            "booking_time":
                                current_time_related_data[
                                    "datetime_string"],
                            "date": current_time_related_data[
                                "date"],
                            "time_zone": current_time_related_data["timezone"],
                            "initial_estimated_cost": estimated_tariff_data["init_amount_in_rs"],
                            "estimated_cost_after_offer": estimated_tariff_data["amount_after_offer"],
                            "estimated_cost": estimated_tariff_data["amount_after_gst"],
                            "tariff_applied": tariff_object.get_tariff_rate(),
                            "offer_applied": tariff_object.get_offer_applied(),
                            "gst": tariff_object.get_gst_rate(),
                            "wallet_recharge": wallet_recharge_data,
                            "current_status": ChargingStatus.BOOKED.name,
                            "charger_status": one_station_data[
                                "station_status"],
                            "station_name": one_station_data["name"],
                            "charger_point_type": one_charger_data["charger_point_type"],
                            "station_address": one_station_data[
                                "address_line"],
                            "avg_rating": one_station_data["rating"]["avg_rating"],
                            "relay_switch_number": relay_switch_number,
                            "reference_transaction_id": reference_transaction_id,
                            "vendor_user_id": vendor_user_id
                            }
    final_data_for_db_update.update(current_dynamic_data)
    return final_data_for_db_update


async def update_session_table(data_communicator, data_to_update_in_session_table):
    parsed_data_to_store_in_db = data_schemas.BookChargingSessionData.parse_obj(data_to_update_in_session_table)
    logger.debug(f"Data for new booking is {parsed_data_to_store_in_db}")
    data_communicator.add_new_entry_in_booking_table(parsed_data_to_store_in_db)
    return parsed_data_to_store_in_db


async def update_charger_status(data_communicator, parsed_data_to_store_in_db):
    data_chunk_to_update_charger_status = data_schemas.ChargingPointDataForUpdate.parse_obj(
        {"station_id": parsed_data_to_store_in_db.station_id,
         "vendor_id": parsed_data_to_store_in_db.vendor_id,
         "charger_point_id": parsed_data_to_store_in_db.charger_point_id,
         "charger_point_status": ChargerStatus.CHARGER_BUSY,
         "connector_point_id": parsed_data_to_store_in_db.connector_point_id,
         "connector_point_status": ChargerStatus.CHARGER_BUSY})
    return data_communicator.update_charger_status_in_agg_table(data_chunk_to_update_charger_status)


async def get_common_data_chunk_to_return_to_user(parsed_data_to_store_in_db: data_schemas.BookChargingSessionData):
    return {
        "vendor_id": parsed_data_to_store_in_db.vendor_id,
        "booking_id": parsed_data_to_store_in_db.booking_id,
        "initial_estimated_cost": parsed_data_to_store_in_db.initial_estimated_cost,
        "estimated_cost_after_offer": parsed_data_to_store_in_db.estimated_cost_after_offer,
        "estimated_cost": parsed_data_to_store_in_db.estimated_cost,
        "wallet_recharge": parsed_data_to_store_in_db.wallet_recharge,
        "tariff_applied": f"{parsed_data_to_store_in_db.tariff_applied}/kwh",
        "offer_applied": parsed_data_to_store_in_db.offer_applied,
        "gst": parsed_data_to_store_in_db.gst,
        "data_to_input_in_step_function": parsed_data_to_store_in_db.dict(),
        "start_charging_data": {
            "station_id": parsed_data_to_store_in_db.station_id,
            "charger_point_id": parsed_data_to_store_in_db.charger_point_id,
            "connector_point_id": parsed_data_to_store_in_db.connector_point_id
         }
    }

