from utility.custom_logger import logger
from fastapi import HTTPException
from vendor_workflow.common_workflows.all_common_utils import prepare_input_data_for_current_function


class ElectroliteBookCharger:
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


class ElectroliteStartCharging:
    def __init__(self, vendor_id, booking_id, running_strategy: list):
        self.start_charge_process_map = {"action": "start", "calling_method": "POST",
                                         "start_charging_data_update_for_session": {
                                             "booking_id": booking_id,
                                             "vendor_id": vendor_id
                                         }}
        self.running_strategy = running_strategy

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


class ElectroliteStopCharging:
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


class ElectroliteStatusCharging:
    def __init__(self, vendor_id, booking_id, socket_connection_id, running_strategy):
        self.status_process_map = {"action": "status", "calling_method": "GET",
                                   "charging_status_data_update": {"booking_id": booking_id,
                                                                   "vendor_id": vendor_id}
                                   }
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
