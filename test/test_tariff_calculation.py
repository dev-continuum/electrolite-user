from unittest import TestCase
from tariff_calculation.tariff_calculator import provide_charging_tariff


class TestTariffs(TestCase):
    def test_chargemod_tariff(self):
        result = provide_charging_tariff("chargemod", 1, 20)
        self.assertEqual(200, result)

