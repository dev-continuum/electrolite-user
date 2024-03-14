import datetime
from unittest import TestCase
from utility.time_calculator import get_current_date_time_format


class TestDateTimeFormats(TestCase):
    def test_utc_date_time_generation(self):
        result = get_current_date_time_format(timezone="UTC", time_format="isoformat")
        self.assertIsInstance(datetime.datetime.fromisoformat(result["datetime_string"]), datetime.datetime)
        self.assertIsInstance(result["date"], str)
        self.assertIsInstance(result["time"], str)
        self.assertIsInstance(result["timezone"], str)


