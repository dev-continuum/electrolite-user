from abc import ABC, abstractmethod
from vendor_workflow import ElectroliteStopCharging, ChargeModStopCharging
from vendor_workflow.common_workflows.stop_charging_common import *
from vendor_workflow.common_workflows.all_common_utils import get_url_params_from_db, ocpi_db_data_parser
from fastapi import HTTPException, status
from data_store.data_organizer import get_data_communicator
from utility.async_third_party_communicator import make_generic_async_http_request


class StopChargingMeta(ABC):
    """Basic representation of START Charging"""

    @abstractmethod
    def stop_charging(self):
        """This method must be implemented for each vendor"""

    @abstractmethod
    def generate_strategy(self):
        """method to generate strategy for booking"""


class StopChargeBaseConstructor(StopChargingMeta):
    def __init__(self, vendor_id, booking_id, stop_charging_data, lambda_client, s3_client, db, sqs):
        self.vendor_id = vendor_id
        self.booking_id = booking_id
        self.stop_charging_data = stop_charging_data
        self.lambda_client = lambda_client
        self.s3_client = s3_client
        self.db = db
        self.sqs = sqs
        self.third_party_communicator = make_generic_async_http_request
        self.data_communicator = get_data_communicator(vendor_id, db, sqs)

    def stop_charging(self):
        pass

    def generate_strategy(self):
        return [
            {"function": get_url_params_from_db, "input_data": [self.data_communicator], "input_keys": None,
             "output_key": "vendor_data"},

            {"function": ocpi_db_data_parser, "input_data": None, "input_keys": ["vendor_data", "action"],
             "output_key": "parsed_vendor_data"},

            {"function": send_request_to_stop_charging, "input_data": [make_generic_async_http_request],
             "input_keys": ["parsed_vendor_data"],
             "output_key": "server_response"},

            {"function": prepare_data_for_db_update_based_on_response, "input_data": None,
             "input_keys": ["server_response", "stop_charging_data_for_session_update"],
             "output_key": "status_data_to_update_db"},

            {"function": prepare_data_for_user, "input_data": None,
             "input_keys": ["server_response", "status_data_to_update_db"], "output_key": "data_for_user"},

            {"function": update_booking_table_for_charge_stop_status, "input_data": [self.data_communicator],
             "input_keys": ["status_data_to_update_db"], "output_key": "db_update_result"},

            {"function": mark_charger_free_in_location_table,
             "input_data": [self.data_communicator, self.vendor_id, self.stop_charging_data], "input_keys": None,
             "output_key": "mark_connector_result"}
        ]


class StopChargeModCharging(StopChargeBaseConstructor):
    def __init__(self, vendor_id, booking_id, stop_charging_data, lambda_client, s3_client, db, sqs):
        super().__init__(vendor_id, booking_id, stop_charging_data, lambda_client, s3_client, db, sqs)
        self.current_strategy = self.generate_local_strategy()

    def generate_local_strategy(self) -> list:
        from vendor_workflow.chargemod_specific_workflow.chargemod_common_support_function import \
            generate_chargemod_header_data, \
            generate_chargemod_stop_body_data
        current_local_strategy = self.generate_strategy()
        current_local_strategy.insert(1, {"function": generate_chargemod_header_data, "input_data": None,
                                          "input_keys": ["vendor_data"],
                                          "output_key": "vendor_data"})
        current_local_strategy.insert(2, {"function": generate_chargemod_stop_body_data,
                                          "input_data": [self.stop_charging_data],
                                          "input_keys": ["vendor_data"],
                                          "output_key": "vendor_data"})
        return current_local_strategy

    async def stop_charging(self):
        stop_chargemod_charging = ChargeModStopCharging(vendor_id=self.vendor_id, booking_id=self.booking_id,
                                                        running_strategy=self.current_strategy)
        return await stop_chargemod_charging.stop_charging()


class StopElectroliteCharging(StopChargeBaseConstructor):
    def __init__(self, vendor_id, booking_id, stop_charging_data, lambda_client, s3_client, db, sqs):
        super().__init__(vendor_id, booking_id, stop_charging_data, lambda_client, s3_client, db, sqs)
        self.current_strategy = self.generate_local_strategy()

    def generate_local_strategy(self) -> list:
        from vendor_workflow.electrolite_specific_workflow.electrolite_common_support_functions import \
            generate_stop_electrolite_body_data, \
            generate_electrolite_header_data
        current_local_strategy = self.generate_strategy()
        current_local_strategy.insert(1, {"function": generate_electrolite_header_data, "input_data": None,
                                          "input_keys": ["vendor_data"],
                                          "output_key": "vendor_data"})
        current_local_strategy.insert(2, {"function": generate_stop_electrolite_body_data,
                                          "input_data": [self.stop_charging_data],
                                          "input_keys": ["vendor_data"],
                                          "output_key": "vendor_data"})
        return current_local_strategy

    async def stop_charging(self):
        stop_electrolite_charging = ElectroliteStopCharging(vendor_id=self.vendor_id, booking_id=self.booking_id,
                                                            running_strategy=self.current_strategy)
        return await stop_electrolite_charging.stop_charging()


def read_stop_charging_factory(vendor_id):
    factories = {
        "chargemod": StopChargeModCharging,
        "electrolite": StopElectroliteCharging
    }
    try:
        stopper = factories[vendor_id]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This vendor id does not exist")
    else:
        return stopper
