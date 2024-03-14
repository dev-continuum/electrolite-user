from abc import ABC, abstractmethod
from vendor_workflow.common_workflows.start_charging_common import *
from vendor_workflow.common_workflows.all_common_utils import get_url_params_from_db, ocpi_db_data_parser
from data_store.data_organizer import get_data_communicator
from utility.async_third_party_communicator import make_generic_async_http_request
from fastapi import HTTPException, status


class StartChargingMeta(ABC):
    """Basic representation of START Charging"""

    @abstractmethod
    def start_charging(self):
        """This method must be implemented for each vendor"""

    @abstractmethod
    def generate_strategy(self):
        """method to generate strategy for booking"""


class StartChargerBaseConstructor(StartChargingMeta):
    def __init__(self, vendor_id, booking_id, start_charging_data, lambda_client, s3_client, db, sqs):
        self.vendor_id = vendor_id
        self.booking_id = booking_id
        self.start_charging_data = start_charging_data
        self.lambda_client = lambda_client
        self.s3_client = s3_client
        self.db = db
        self.sqs = sqs
        self.third_party_communicator = make_generic_async_http_request
        self.data_communicator = get_data_communicator(vendor_id, db, sqs)

    def start_charging(self):
        pass

    def generate_strategy(self):
        return [
            {"function": get_booking_details, "input_keys": None,
             "input_data": [self.booking_id, self.data_communicator],
             "output_key": "booking_data"},

            {"function": check_for_booking_id_usage, "input_data": None, "input_keys": ["booking_data"],
             "output_key": "proceed_further"},

            {"function": get_url_params_from_db, "input_data": [self.data_communicator], "input_keys": None,
             "output_key": "vendor_data"},

            # Insert header body data manipulation for specific vendor here

            {"function": ocpi_db_data_parser, "input_data": None, "input_keys": ["vendor_data", "action"],
             "output_key": "parsed_vendor_data"},

            {"function": send_request_to_start_charging,
             "input_data": [self.start_charging_data, self.third_party_communicator],
             "input_keys": ["parsed_vendor_data", "calling_method"], "output_key": "server_response"},

            {"function": prepare_data_for_db_update_based_on_response, "input_data": None,
             "input_keys": ["server_response", "start_charging_data_update_for_session"],
             "output_key": "parsed_data_for_db"},

            {"function": update_booking_table_for_charge_start_status, "input_data": [self.data_communicator],
             "input_keys": ["parsed_data_for_db"], "output_key": "db_update_result"},

            {"function": prepare_data_for_user, "input_data": [self.start_charging_data],
             "input_keys": ["server_response", "parsed_data_for_db"],
             "output_key": "data_for_user"}
        ]


class StartChargeModCharging(StartChargerBaseConstructor):
    def __init__(self, vendor_id, booking_id, start_charging_data, lambda_client, s3_client, db, sqs):
        super().__init__(vendor_id, booking_id, start_charging_data, lambda_client, s3_client, db, sqs)
        self.current_strategy = self.generate_local_strategy()

    def generate_local_strategy(self) -> list:
        from vendor_workflow.chargemod_specific_workflow.chargemod_common_support_function import \
            generate_chargemod_header_data, generate_chargemod_start_body_data
        current_local_strategy = self.generate_strategy()
        current_local_strategy.insert(3, {"function": generate_chargemod_header_data, "input_data": None,
                                          "input_keys": ["vendor_data"],
                                          "output_key": "vendor_data"})
        current_local_strategy.insert(4, {"function": generate_chargemod_start_body_data,
                                          "input_data": [self.start_charging_data],
                                          "input_keys": ["vendor_data"],
                                          "output_key": "vendor_data"})
        return current_local_strategy

    def start_charging(self):
        from vendor_workflow import ChargeModStartCharging
        start_chargemod_charging = ChargeModStartCharging(vendor_id=self.vendor_id, booking_id=self.booking_id,
                                                          running_strategy=self.current_strategy)
        return start_chargemod_charging.start_charging()


class StartElectroliteCharging(StartChargerBaseConstructor):

    def __init__(self, vendor_id, booking_id, start_charging_data, lambda_client, s3_client, db, sqs):
        super().__init__(vendor_id, booking_id, start_charging_data, lambda_client, s3_client, db, sqs)
        self.current_strategy = self.generate_local_strategy()

    def generate_local_strategy(self) -> list:
        from vendor_workflow.electrolite_specific_workflow.electrolite_common_support_functions import \
            generate_start_electrolite_body_data, \
            generate_electrolite_header_data
        current_local_strategy = self.generate_strategy()
        current_local_strategy.insert(3, {"function": generate_electrolite_header_data, "input_data": None,
                                          "input_keys": ["vendor_data"],
                                          "output_key": "vendor_data"})
        current_local_strategy.insert(4, {"function": generate_start_electrolite_body_data,
                                          "input_data": [self.start_charging_data],
                                          "input_keys": ["vendor_data"],
                                          "output_key": "vendor_data"})

        return current_local_strategy

    def start_charging(self):
        from vendor_workflow import ElectroliteStartCharging
        start_electrolite_charging = ElectroliteStartCharging(vendor_id=self.vendor_id, booking_id=self.booking_id,
                                                              running_strategy=self.current_strategy)
        return start_electrolite_charging.start_charging()


def read_start_charging_factory(vendor_id):
    factories = {
        "chargemod": StartChargeModCharging,
        "electrolite": StartElectroliteCharging
    }
    try:
        starter = factories[vendor_id]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This vendor id does not exist")
    else:
        return starter
