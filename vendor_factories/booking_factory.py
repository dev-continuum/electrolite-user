from abc import ABC, abstractmethod
from vendor_workflow.common_workflows.book_charger_common import *
from vendor_workflow.common_workflows.all_common_utils import get_user_selected_vehicle_data, get_url_params_from_db
from fastapi import HTTPException, status
from wallet_service.wallet_service import ReadUserWalletBalance
from data_store.data_organizer import get_data_communicator
from utility.time_calculator import get_current_date_time_format
from app.user_operations.check_user_booking_data import CheckUserBookings


class BookChargerMeta(ABC):
    """Basic representation of BOOK Charger"""

    @abstractmethod
    def book_charger(self):
        """This method must be implemented for each vendor"""

    @abstractmethod
    def generate_strategy(self):
        """method to generate strategy for booking"""


class BookChargerBaseConstructor(BookChargerMeta):
    """
    Common class for booking a charger
    All vendor specific classed are supposed to inherit from this class
    to get the common functionalities related to booking
    """
    def __init__(self, book_charger_data, db, sqs, current_user, s3_client):
        self.book_charger_data = book_charger_data
        self.db = db
        self.sqs = sqs
        self.current_user = current_user
        self.s3_client = s3_client
        self.data_communicator_object = get_data_communicator(book_charger_data.vendor_id, db, sqs)
        self.current_time_related_data = get_current_date_time_format(timezone="UTC", time_format="isoformat")
        self.one_station_data = self.data_communicator_object.get_one_station_data_from_agg_table(
            station_id=self.book_charger_data.station_id)
        self.available_chargers = self.one_station_data["total_charger_data"]
        self.current_vehicle_data_for_booking = get_user_selected_vehicle_data(book_charger_data,
                                                                               current_user.vehicle_data)
        self.check_user_bookings = CheckUserBookings(db=db, current_user=current_user,
                                                     book_charger_data=book_charger_data)
        self.wallet_balance = ReadUserWalletBalance(user_id=self.current_user.phonenumber).read_wallet_data_for_given_user()["data"][
                "wallet"]

    def book_charger(self):
        """Putting placeholder method to satisfy metaclass requirements"""
        pass

    def generate_strategy(self) -> list:
        return [{"function": check_charger_status, "input_keys": None,
                 "input_data": [self.available_chargers, self.book_charger_data],
                 "output_key": "charger_status"},

                {"function": strategy_decision, "input_keys": ["charger_status"],
                 "input_data": [self.check_user_bookings],
                 "output_key": "proceed_further"},

                {"function": get_url_params_from_db, "input_data": [self.data_communicator_object],
                 "input_keys": None, "output_key": "vendor_data"},

                {"function": get_tariff_object, "input_data": [self.book_charger_data],
                 "input_keys": ["vendor_data"], "output_key": "tariff_object"},

                {"function": prepare_static_data_for_db_update,
                 "input_keys": None,
                 "input_data": [self.book_charger_data,
                                self.current_vehicle_data_for_booking],
                 "output_key": "static_data_to_update_db"},

                {"function": get_current_charger_power_capacity,
                 "input_keys": None,
                 "input_data": [self.book_charger_data, self.available_chargers],
                 "output_key": "power_in_kw"},

                {"function": get_estimated_tariff, "input_keys": ["power_in_kw", "tariff_object"],
                 "input_data": [self.book_charger_data, self.current_vehicle_data_for_booking],
                 "output_key": "estimated_tariff_data"},

                {"function": get_current_wallet_recharge_details,
                 "input_keys": ["estimated_tariff_data"],
                 "input_data": [self.wallet_balance],
                 "output_key": "wallet_recharge_data"},

                {
                    "function": generate_and_update_dynamic_data_for_session,
                    "input_keys": ["charger_status", "static_data_to_update_db", "estimated_tariff_data",
                                   "wallet_recharge_data", "tariff_object"],
                    "input_data": [self.current_time_related_data, self.one_station_data],
                    "output_key": "data_to_update_in_session_table"},

                {"function": update_session_table,
                 "input_keys": ["data_to_update_in_session_table"],
                 "input_data": [self.data_communicator_object],
                 "output_key": "parsed_data_to_store_in_db"},

                {"function": update_charger_status,
                 "input_keys": ["parsed_data_to_store_in_db"],
                 "input_data": [self.data_communicator_object],
                 "output_key": "charger_status_change_result"},

                {"function": get_common_data_chunk_to_return_to_user,
                 "input_keys": ["parsed_data_to_store_in_db"],
                 "input_data": [],
                 "output_key": "data_for_user"}]


class BookChargeModCharger(BookChargerBaseConstructor):

    def __init__(self, book_charger_data, db, sqs, current_user, s3_client):
        super().__init__(book_charger_data, db, sqs, current_user, s3_client)
        self.current_strategy = self.generate_local_strategy()

    def modify_dynamic_data_generation_strategy_input(self, current_common_strategy):
        for strategy in current_common_strategy:
            if strategy["function"].__name__ == "generate_and_update_dynamic_data_for_session":
                logger.info(f"modifying strategy {strategy['function'].__name__} for the chargemod")
                strategy["input_keys"].append("relay_switch_number")
                strategy["input_keys"].append("transaction_id")
                strategy["input_keys"].append("vendor_user_id")
        return current_common_strategy

    def generate_local_strategy(self) -> list:
        # importing specific methods for chargemod to insert in to the strategy
        from vendor_workflow.chargemod_specific_workflow.chargemod import get_relay_number, get_latest_transaction_id, get_vendor_user_id
        from vendor_workflow.chargemod_specific_workflow.chargemod_common_support_function import modify_response_data_as_per_chargemod

        current_common_strategy = self.generate_strategy()
        # #######Inserting 3 specific functionalities specific to chargemod ##############
        current_common_strategy.insert(3, {"function": get_vendor_user_id,
                                           "input_keys": ["vendor_data"],
                                           "input_data": None,
                                           "output_key": "vendor_user_id"})

        current_common_strategy.insert(4, {"function": get_relay_number,
                                           "input_keys": None,
                                           "input_data": [self.available_chargers,
                                                          self.book_charger_data],
                                           "output_key": "relay_switch_number"})

        current_common_strategy.insert(5, {"function": get_latest_transaction_id,
                                           "input_keys": None,
                                           "input_data": [self.data_communicator_object],
                                           "output_key": "transaction_id"})

        current_common_strategy.append({"function": modify_response_data_as_per_chargemod,
                                        "input_keys": ["parsed_data_to_store_in_db", "data_for_user"],
                                        "input_data": None,
                                        "output_key": "data_for_user"})
        # Modifying one existing strategy to insert the inputs generated by chargemode specific functions
        current_common_strategy = self.modify_dynamic_data_generation_strategy_input(current_common_strategy)

        return current_common_strategy

    def book_charger(self):
        # Importing Chargemod Booking class
        from vendor_workflow import ChargeModBookCharger
        chargemod_booking = ChargeModBookCharger(running_strategy=self.current_strategy)
        return chargemod_booking.book_charger()


class BookElectroliteCharger(BookChargerBaseConstructor):
    def __init__(self, book_charger_data, db, sqs, current_user, s3_client):
        super().__init__(book_charger_data, db, sqs, current_user, s3_client)
        self.current_strategy = self.generate_local_strategy()

    def generate_local_strategy(self) -> list:
        from vendor_workflow.electrolite_specific_workflow.electrolite_common_support_functions import modify_response_data_as_per_electrolite
        current_common_strategy = self.generate_strategy()
        current_common_strategy.append({"function": modify_response_data_as_per_electrolite,
                                        "input_keys": ["parsed_data_to_store_in_db", "data_for_user"],
                                        "input_data": None,
                                        "output_key": "data_for_user"})
        return current_common_strategy

    def book_charger(self):
        from vendor_workflow import ElectroliteBookCharger
        electrolite_booking = ElectroliteBookCharger(running_strategy=self.current_strategy)
        return electrolite_booking.book_charger()


def read_booking_factory(vendor_id):
    factories = {
        "chargemod": BookChargeModCharger,
        "electrolite": BookElectroliteCharger
    }
    try:
        booker = factories[vendor_id]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This vendor id does not exist")
    else:
        return booker
