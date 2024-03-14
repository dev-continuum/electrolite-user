from abc import ABC, abstractmethod
from vendor_workflow.common_workflows.status_charging_vendor_common import *
from vendor_workflow.common_workflows.all_common_utils import get_url_params_from_db, ocpi_db_data_parser
from data_store.data_organizer import get_data_communicator
from utility.async_third_party_communicator import make_generic_async_http_request
from fastapi import HTTPException, status


class StatusChargingMeta(ABC):
    """Basic representation of START Charging"""

    @abstractmethod
    def status_charging(self):
        """This method must be implemented for each vendor"""

    @abstractmethod
    def generate_strategy(self):
        """method to generate strategy for booking"""


class StatusChargingBaseConstructor(StatusChargingMeta):
    def __init__(self, vendor_id, booking_id, charging_status_data, socket_connection_id, lambda_client, s3_client, db,
                 sqs):
        self.vendor_id = vendor_id
        self.booking_id = booking_id
        self.socket_connection_id = socket_connection_id
        self.charging_status_data = charging_status_data
        self.lambda_client = lambda_client
        self.s3_client = s3_client
        self.db = db
        self.sqs = sqs
        self.third_party_communicator = make_generic_async_http_request
        self.data_communicator = get_data_communicator(vendor_id, db, sqs)

    def status_charging(self):
        pass

    def generate_strategy(self):
        return [
            {"function": get_url_params_from_db, "input_data": [self.data_communicator], "input_keys": None,
             "output_key": "vendor_data"},
            # Insert vendor specific header body data manipulation here

            {"function": ocpi_db_data_parser, "input_data": None, "input_keys": ["vendor_data", "action"],
             "output_key": "parsed_vendor_data"},

            {"function": send_request_for_charging_status, "input_data": [self.third_party_communicator],
             "input_keys": ["parsed_vendor_data"], "output_key": "server_response"},

            {"function": calculate_live_stats_based_on_response, "input_data": [self.charging_status_data],
             "input_keys": ["server_response"], "output_key": "updated_response"},

            {"function": prepare_data_for_db_update_based_on_response, "input_data": None,
             "input_keys": ["updated_response", "charging_status_data_update"],
             "output_key": "charging_status_data_update_for_session"},

            {"function": update_booking_table_for_charging_status, "input_data": [self.data_communicator],
             "input_keys": ["charging_status_data_update_for_session"], "output_key": "data_returned_from_db"},

            {"function": prepare_data_for_internal_user, "input_data": [],
             "input_keys": ["server_response", "data_returned_from_db"], "output_key": "data_for_user"}
        ]


class StatusChargeModCharging(StatusChargingBaseConstructor):
    def __init__(self, vendor_id, booking_id, charging_status_data, socket_connection_id, lambda_client, s3_client, db,
                 sqs):
        super().__init__(vendor_id, booking_id, charging_status_data, socket_connection_id, lambda_client, s3_client,
                         db, sqs)
        self.current_strategy = self.generate_local_strategy()

    def generate_local_strategy(self) -> []:
        from vendor_workflow.chargemod_specific_workflow.chargemod_common_support_function import \
            generate_chargemod_header_data, \
            generate_chargemod_status_body_data
        current_local_strategy = self.generate_strategy()
        current_local_strategy.insert(1, {"function": generate_chargemod_header_data, "input_data": None,
                                          "input_keys": ["vendor_data"],
                                          "output_key": "vendor_data"})
        current_local_strategy.insert(2, {"function": generate_chargemod_status_body_data,
                                          "input_data": [self.charging_status_data],
                                          "input_keys": ["vendor_data"],
                                          "output_key": "vendor_data"})
        return current_local_strategy

    def status_charging(self):
        from vendor_workflow import ChargeModStatusCharging
        status_chargemod_charging = ChargeModStatusCharging(vendor_id=self.vendor_id, booking_id=self.booking_id,
                                                            socket_connection_id=self.socket_connection_id,
                                                            running_strategy=self.current_strategy)
        return status_chargemod_charging.status_charging()


class StatusElectroliteCharging(StatusChargingBaseConstructor):
    def __init__(self, vendor_id, booking_id, charging_status_data, socket_connection_id, lambda_client, s3_client, db,
                 sqs):
        super().__init__(vendor_id, booking_id, charging_status_data, socket_connection_id, lambda_client, s3_client,
                         db, sqs)
        self.current_strategy = self.generate_local_strategy()

    def generate_local_strategy(self) -> list:
        from vendor_workflow.electrolite_specific_workflow.electrolite_common_support_functions import \
            generate_status_electrolite_body_data, \
            generate_electrolite_header_data
        current_local_strategy = self.generate_strategy()
        current_local_strategy.insert(1, {"function": generate_electrolite_header_data, "input_data": None,
                                          "input_keys": ["vendor_data"],
                                          "output_key": "vendor_data"})
        current_local_strategy.insert(2, {"function": generate_status_electrolite_body_data,
                                          "input_data": [self.charging_status_data],
                                          "input_keys": ["vendor_data"],
                                          "output_key": "vendor_data"})

        return current_local_strategy

    def status_charging(self):
        from vendor_workflow import ElectroliteStatusCharging
        status_electrolite_charging = ElectroliteStatusCharging(vendor_id=self.vendor_id, booking_id=self.booking_id,
                                                                socket_connection_id=self.socket_connection_id,
                                                                running_strategy=self.current_strategy
                                                                )
        return status_electrolite_charging.status_charging()


def read_status_charging_factory(vendor_id):
    factories = {
        "chargemod": StatusChargeModCharging,
        "electrolite": StatusElectroliteCharging
    }
    try:
        updater = factories[vendor_id]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This vendor id does not exist")
    else:
        return updater
