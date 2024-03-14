from utility.custom_logger import logger as logging
import requests
import random
from app import get_db, settings
from data_store import data_schemas, crud
from data_store.database import create_tables
from fastapi import HTTPException, status
import json
import os
import pathlib


def translate_connection_id(connection_details, ref_data):
    for item in ref_data["ConnectionTypes"]:
        if item["ID"] == connection_details["ConnectionTypeID"]:
            return item["Title"]


def translate_connection_status(connection_details, ref_data):
    for item in ref_data["StatusTypes"]:
        if item["ID"] == connection_details["StatusTypeID"]:
            return item["Title"]


def get_data_from_open_charge_api(lat=None, long=None, country="IN", max_result=20, ref_data=None):
    list_of_parsed_locations = list()
    list_of_location_json = list()
    params = {"latitude": lat, "longitude": long, "countrycode": country,
              "output": "json", "compact": True, "maxresults": max_result,
              'key': 'f9479a4f-adf6-4c34-bc0a-26aed29c2346]'}
    try:
        base_url = 'https://api.openchargemap.io/v3/poi/?'
        location_results = requests.get(base_url, params=params)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not able to fetch data from open charge api")
    else:
        count = 1
        for address in location_results.json():
            current_address = address["AddressInfo"]
            connection_details = address["Connections"][0]
            # Todo: DummyAlert putting local data in first two station ids
            if count == 1:
                address["UUID"] = settings.STATION1
            elif count == 2:
                address["UUID"] = settings.STATION2
            else:
                break
            try:
                mapper = {
                    "station_id": address["UUID"],
                    "station_time": {"start_time": "12:00 AM", "end_time": "11:59 PM"},
                    "title": current_address["Title"],
                    "address_line": current_address["AddressLine1"],
                    "town": current_address["Town"],
                    "state": current_address["StateOrProvince"],
                    "postal_code": current_address["Postcode"],
                    "country_id": current_address["CountryID"],
                    "latitude": current_address["Latitude"],
                    "longitude": current_address["Longitude"],
                    "distance_unit": current_address["DistanceUnit"],
                    # TODO: DummyAlert: send actual charger status after taking from stations
                    "available_chargers": [{"charger_point_id": 1, "connector_point_id": 1,
                                            "charger_point_type": "Chademo", "Status": "Available", "tariff": 125,
                                            "power_capacity": 50},
                                           {"charger_point_id": 2, "connector_point_id": 1, "charger_point_type": "CC2",
                                            "Status": "Available", "tariff": 125,
                                            "power_capacity": 150}],
                    "connection_type_id": translate_connection_id(connection_details, ref_data),
                    "connection_status_type_id": translate_connection_status(connection_details, ref_data),
                    "connection_point_quantity": connection_details["Quantity"],
                    "total_connectors_available": address["NumberOfPoints"]
                }

            except Exception as e:
                logging.exception("Error during the translation of openapi data")
                # raise HTTPException(
                #     status_code=status.HTTP_404_NOT_FOUND,
                #     detail="Some data is missing during mapping")
            else:
                mapped_data = data_schemas.ChargingStationStaticData.parse_obj(mapper)
                list_of_parsed_locations.append(mapped_data)
                list_of_location_json.append(mapper)
            finally:
                count += 1

    # TODO: Major very expensive task think about better solution later
    for station in list_of_parsed_locations:
        crud.add_new_station(get_db(), station)
    return list_of_parsed_locations


# def get_data_from_station_json(station_id):
#     path_to_open = pathlib.Path.joinpath(pathlib.Path(__file__).parent.resolve(), "station_data.json")
#     try:
#         with open(path_to_open, "r") as fh:
#             station_data = json.load(fh)
#             for item in station_data:
#                 if item["station_id"] == station_id:
#                     return item
#             else:
#                 return {}
#     except FileNotFoundError:
#         # TODO: This is bad design make sure data is fetched through db
#         get_data_from_open_charge_api(lat=12.864970, long=77.655067, country="IN", ref_data=get_reference_data())
#         with open(path_to_open, "r") as fh:
#             station_data = json.load(fh)
#             for item in station_data:
#                 if item["station_id"] == station_id:
#                     return item
#             else:
#                 return {}
#

def add_data_to_static_table():
    create_tables()
    db = get_db()
    list_of_parsed_locations = get_data_from_open_charge_api(lat=12.864970, long=77.655067, country="IN",
                                                             ref_data=get_reference_data())
    for station in list_of_parsed_locations:
        crud.add_new_station(get_db(), station)


def get_reference_data():
    params = {'key': 'f9479a4f-adf6-4c34-bc0a-26aed29c2346]'}
    base_url = 'https://api.openchargemap.io/v3/referencedata/?'
    logging.info("getting reference data for open api")
    reference_data = requests.get(base_url, params=params).json()
    return reference_data


if __name__ == '__main__':
    #print(get_data_from_open_charge_api(lat=12.864970, long=77.655067, country="IN", ref_data=get_reference_data()))
    add_data_to_static_table()
