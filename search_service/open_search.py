import json
import aiohttp
import simplejson
from fastapi import HTTPException, status
from config import Settings
from data_store.data_schemas import ChargingStationLocationBasedData, ChargingStationSearchData
from utility.async_third_party_communicator import make_async_http_request
from utility.custom_logger import logger

settings: Settings = Settings()

open_search_url = settings.SEARCH_SERVICE_URL


def prepare_list_of_stations(station_data) -> []:
    list_of_stations = []
    try:
        station_data = simplejson.loads(station_data)
        for record in station_data["records"]:
            list_of_stations.append(record["charge_station"])
    except simplejson.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Unable to decode received data")
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Search result not able to fetch records")
    else:
        return list_of_stations


async def get_stations_based_on_long_lat_only(location_related_data: ChargingStationLocationBasedData) -> []:
    logger.info("Getting stations list based on location only")
    request_body = {
        "offset": location_related_data.offset,
        "limit": location_related_data.limit,
        "location": [
            location_related_data.lat,
            location_related_data.long
        ],
        "proximity_in_km": location_related_data.proximity_in_km,
    }
    try:
        response = await make_async_http_request(url=open_search_url, body=request_body)
    except HTTPException:
        raise
    else:
        return prepare_list_of_stations(response)


async def filter_stations_based_on_search_terms(location_related_data: ChargingStationLocationBasedData,
                                                search_data: ChargingStationSearchData) -> []:
    logger.info("Filtering stations list based on filter parameters")
    if search_data.distance > 0:
        current_distance = search_data.distance
    else:
        current_distance = location_related_data.proximity_in_km
    logger.debug(f"Current distance parameter is {current_distance}")

    dict_search_data = search_data.dict(exclude_defaults=True)
    # del (dict_search_data["distance"])

    request_body = {
                "offset": location_related_data.offset,
                "limit": location_related_data.limit,
                "location": [
                    location_related_data.lat,
                    location_related_data.long
                ],
                "proximity_in_km": current_distance,
                "search_by": dict_search_data
            }
    try:
        response = await make_async_http_request(url=open_search_url, body=request_body)
    except HTTPException:
        raise
    else:
        return prepare_list_of_stations(response)


async def universal_search(location_related_data: ChargingStationLocationBasedData, search_string) -> []:
    logger.info("Getting stations list based on search strings")
    search_data: ChargingStationSearchData = ChargingStationSearchData.parse_obj({"text": search_string})
    request_body = {
                "offset": location_related_data.offset,
                "limit": location_related_data.limit,
                "location": [
                    location_related_data.lat,
                    location_related_data.long
                ],
                "proximity_in_km": location_related_data.proximity_in_km,
                "search_by": search_data.dict(exclude_defaults=True)
            }
    try:
        response = await make_async_http_request(url=open_search_url, body=request_body)
    except HTTPException:
        raise
    else:
        return prepare_list_of_stations(response)
