from utility.custom_logger import logger as logging
from fastapi import status
from data_store import crud, data_schemas


def station_key_error_handler(db, station_id):
    station_details = crud.get_one_station_data(db, station_id)
    if len(station_details) == 0:
        return {"status_code": status.HTTP_404_NOT_FOUND, "message": f"This station is not available",
                "data": {}}
    else:
        return {"status_code": status.HTTP_404_NOT_FOUND, "message": f"Charger is unavailable. Current status is "
                                                                     f"{station_details[0]['evse_status'].lower()}",
                "data": {}}
