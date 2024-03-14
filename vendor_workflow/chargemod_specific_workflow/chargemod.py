from data_store import data_schemas
from utility.custom_logger import logger
from fastapi import HTTPException
from utility.async_third_party_communicator import make_generic_async_http_request
from data_store.data_organizer import DataCommunicator
from vendor_workflow.common_workflows.all_common_utils import prepare_input_data_for_current_function

"""
Diff for booking chargemod charger
1- vendor id user id from db
2- relay number logic in booking class
3- unique reference_transaction_id in booking class

"""


async def get_vendor_user_id(vendor_data):
    return vendor_data["user_id"]


async def get_relay_number(available_chargers, book_charger_data):
    relay_switch_number = None
    for charger in available_chargers:
        if charger["charger_point_id"] == book_charger_data.charger_point_id:
            for connector in charger["connectors"]:
                if connector["connector_point_id"] == book_charger_data.connector_point_id:
                    relay_switch_number = connector["relay_switch_number"]
                    break
    return relay_switch_number


async def get_latest_transaction_id(data_communicator_object):
    previous_transaction_id: int = data_communicator_object.get_vendor_details_from_vendor_db()[
        "reference_transaction_id"]
    current_transaction_id = previous_transaction_id + 1
    data_communicator_object.set_vendor_transaction_id_to_vendor_db(current_transaction_id)
    return current_transaction_id


class ChargeModBookCharger:
    def __init__(self, running_strategy: list):
        self.book_charge_process_map = {}
        self.running_strategy = running_strategy

    async def book_charger(self):
        for step in self.running_strategy:
            logger.info(f"Current step is {step['function'].__name__}")
            final_input_data_list = prepare_input_data_for_current_function(step["input_data"], step["input_keys"],
                                                                            self.book_charge_process_map)
            try:
                self.book_charge_process_map[step["output_key"]] = await step["function"](*final_input_data_list)
            except HTTPException:
                logger.exception("Start charging process failed")
                raise
            logger.info(f"current start charge process map is {self.book_charge_process_map}")
        return self.book_charge_process_map["data_for_user"]


class ChargeModStartCharging:

    def __init__(self, vendor_id, booking_id, running_strategy: list):
        self.start_charge_process_map = {"action": "start", "calling_method": "POST"}
        self.running_strategy = running_strategy
        self.start_charge_process_map["start_charging_data_update_for_session"] = {
            "booking_id": booking_id,
            "vendor_id": vendor_id
        }

    async def start_charging(self):
        for step in self.running_strategy:
            logger.info(f"Current step is {step['function'].__name__}")
            final_input_data_list = prepare_input_data_for_current_function(step["input_data"], step["input_keys"],
                                                                            self.start_charge_process_map)
            try:
                self.start_charge_process_map[step["output_key"]] = await step["function"](*final_input_data_list)
            except HTTPException:
                logger.exception("Start charging process failed")
                raise
            logger.info(f"current start charge process map is {self.start_charge_process_map}")
        return self.start_charge_process_map["data_for_user"]


class ChargeModStopCharging:
    def __init__(self, vendor_id, booking_id, running_strategy: list):
        self.stop_charge_process_map = {"action": "stop", "calling_method": "POST",
                                        "stop_charging_data_for_session_update": {"booking_id": booking_id,
                                                                                  "vendor_id": vendor_id}}
        self.running_strategy = running_strategy

    async def stop_charging(self):
        for step in self.running_strategy:
            logger.info(f"Current step is {step['function'].__name__}")
            final_input_data_list = prepare_input_data_for_current_function(step["input_data"], step["input_keys"],
                                                                            self.stop_charge_process_map)
            try:
                self.stop_charge_process_map[step["output_key"]] = await step["function"](*final_input_data_list)
            except HTTPException:
                logger.exception("Start charging process failed")
                raise
            logger.info(f"current start charge process map is {self.stop_charge_process_map}")
        return self.stop_charge_process_map["data_for_user"]


class ChargeModStatusCharging:
    def __init__(self, vendor_id, booking_id, socket_connection_id, running_strategy):
        self.status_process_map = {"action": "status", "calling_method": "GET",
                                   "charging_status_data_update": {"booking_id": booking_id,
                                                                   "vendor_id": vendor_id}}
        self.running_strategy = running_strategy
        if socket_connection_id:
            self.status_process_map["charging_status_data_update"].update(
                {"socket_connection_id": socket_connection_id})

    async def status_charging(self):
        for step in self.running_strategy:
            logger.info(f"Current step is {step['function'].__name__}")
            final_input_data_list = prepare_input_data_for_current_function(step["input_data"], step["input_keys"],
                                                                            self.status_process_map)
            try:
                self.status_process_map[step["output_key"]] = await step["function"](*final_input_data_list)
            except HTTPException:
                logger.exception("Status charging process failed")
                raise
            logger.info(f"current start charge process map is {self.status_process_map}")
        return self.status_process_map["data_for_user"]
