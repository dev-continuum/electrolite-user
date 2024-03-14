from unittest import TestCase
from utility.step_function_communicator import StepFunctionCommunicator
from decimal import Decimal
import simplejson
from app import get_step_function


class TestTariffs(TestCase):
    def setUp(self) -> None:
        self.test_data = {'booking_time': '2022-10-10 07:44:41', 'booking_id': '91fc9dfb-a57e-40dd-870f-8836882883e9',
                          'vendor_id': 'chargemod', 'date': '2022-10-10', 'calculation_method': 'TIME', 'reference_transaction_id': 61,
                          'vendor_user_id': 12, 'user_id': '9810936621', 'station_id': '110', 'charger_point_id': 1,
                          'connector_point_id': 1, 'charging_activity_id': None, 'charger_status': 'healthy', 'payment_mode': '',
                          'vehicle_used': None, 'target_duration_timestamp': '00:10:00', 'target_energy_kw': Decimal('0'),
                          'estimated_cost': Decimal('100.0'), 'tariff_applied': Decimal('10'), 'station_name': 'BB Test',
                          'station_address': 'chargemod', 'charger_type': '', 'otp': None, 'start_time': None, 'end_time': None,
                          'time_zone': 'UTC', 'start_charging_status': False, 'battery_status': None, 'emission_saved': None,
                          'current_status': 'BOOKED', 'meter_values': None, 'charging_states': {}, 'current_energy_consumed': Decimal('0'),
                          'current_charging_timer': None, 'final_duration_timestamp': None, 'final_energy_consumed': Decimal('0'),
                          'final_cost': Decimal('0'), 'stop_charging_status': False}

        self.step_function = StepFunctionCommunicator(step_client=get_step_function(), data_to_parse_and_input=self.test_data)

    def test_input_data_parsing(self):
        result = self.step_function.parse_data_for_input()
        self.assertEqual(2, len(simplejson.loads(result)))

    def test_send_data_to_step_function(self):
        result = self.step_function.start_step_function()
        self.assertEqual(result['ResponseMetadata']['HTTPStatusCode'], 200)




