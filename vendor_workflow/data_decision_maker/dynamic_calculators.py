
def calculate_current_emission_saved(response_data, vehicle_details) -> {}:
    return {"emission_saved": 20}


def calculate_current_battery_status(response_data) -> {}:
    return {"battery_status" : response_data["meter_values"]["SoC"]}


def calculate_current_range(response_data, vehicle_details) -> {}:
    current_energy_in_kwh = int(response_data["meter_values"]["SoC"]) * float(vehicle_details["power_capacity"])
    current_range = (float(vehicle_details["electric_energy_consumption"])/100)*current_energy_in_kwh
    return {"current_range": current_range}

