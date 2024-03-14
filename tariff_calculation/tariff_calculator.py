# TODO: Dummy Alert use actual data here
import datetime
from utility.time_calculator import convert_time_stamp_to_time_delta
from utility.custom_logger import logger
import locale
from pydantic import BaseModel


# Range (Km)	140
# Max. Speed (Km/Hr)	80
# Acceleration (m/s2)	1.04
# Warranty (In Years)	3
# Electric Energy consumption (KWh per 100KM)	13.3
# Battery
# Battery Technology	Lithium ion
# Battery Capacity (kWh)	16.2
# Battery Density (Wh/Kg)	121
# Battery cycle (No. of Cycles)	2000

class TariffData(BaseModel):
    tariff: float
    unit: str


class Tariff:
    def __init__(self, vendor_id, tariff_data):
        self.vendor = vendor_id
        self.tariff_data = TariffData.parse_obj(tariff_data)

    def get_offer_applied(self):
        return 10

    def get_gst_rate(self):
        return 5
    def format_currency(self, amount):
        locale.setlocale(locale.LC_MONETARY, 'en_IN')
        return float(locale.currency(amount, grouping=True)[1:])

    def apply_offer(self, init_amount_in_rs):
        current_offer = self.get_offer_applied()
        if current_offer:
            amount_after_offer = init_amount_in_rs - init_amount_in_rs * (current_offer / 100)
            logger.debug(f"Cost after offer application is {amount_after_offer}")
            return amount_after_offer
        else:
            return init_amount_in_rs
    def apply_gst(self, amount_after_offer):
        current_gst = self.get_gst_rate()
        if current_gst:
            amount_after_gst = amount_after_offer + current_gst
            logger.debug(f"Cost after gst application is {amount_after_gst}")
            return amount_after_gst
        else:
            return amount_after_offer

    def apply_time_based_calculation_formula(self, time_duration_in_hour, target_station_data_power_in_kw):
        init_amount_in_rs = time_duration_in_hour * target_station_data_power_in_kw * self.tariff_data.tariff
        logger.info(f"duration time stamp {time_duration_in_hour} provided. initial calculated tariff is {init_amount_in_rs}")
        return init_amount_in_rs

    def apply_energy_based_calculation_formula(self, vehicle_battery_capacity_in_kwh, target_station_data_power_in_kw,
                                               energy_needed_in_kw):
        time_required_to_complete_fill = vehicle_battery_capacity_in_kwh / target_station_data_power_in_kw
        amount_in_rs = (time_required_to_complete_fill / vehicle_battery_capacity_in_kwh) * energy_needed_in_kw * self.tariff_data.tariff
        logger.info(f"energy target {energy_needed_in_kw} provided. Estimated tariff is {amount_in_rs}")
        return amount_in_rs

    def calculate_estimated_tariff(self, duration_time_stamp: str = None, energy_needed_in_kw=None,
                                   target_vehicle_data=None, target_station_power_in_kw=None):
        vehicle_battery_capacity_in_kwh = float(target_vehicle_data["power_capacity"])
        if duration_time_stamp:
            time_duration_in_hour = convert_time_stamp_to_time_delta(duration_time_stamp).total_seconds() / (60 * 60)

            init_amount_in_rs = self.apply_time_based_calculation_formula(time_duration_in_hour=time_duration_in_hour,
                                                  target_station_data_power_in_kw=target_station_power_in_kw)


        elif energy_needed_in_kw:
            init_amount_in_rs = self.apply_energy_based_calculation_formula(target_station_data_power_in_kw=target_station_power_in_kw,
                                                                            vehicle_battery_capacity_in_kwh=vehicle_battery_capacity_in_kwh,
                                                                            energy_needed_in_kw=energy_needed_in_kw)


        amount_after_offer = self.apply_offer(init_amount_in_rs)
        amount_after_gst = self.apply_gst(amount_after_offer)
        return {"init_amount_in_rs": self.format_currency(init_amount_in_rs), "amount_after_offer": self.format_currency(amount_after_offer),
                "amount_after_gst": self.format_currency(amount_after_gst)}

    def get_tariff_rate(self):
        logger.debug(f"Providing tariff data for vendor {self.vendor}: {self.tariff_data.tariff}")
        return self.tariff_data.tariff



