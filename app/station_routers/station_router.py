from .. import get_db, get_lambda, get_s3, get_sqs, get_step_function, settings
from search_service.open_search import get_stations_based_on_long_lat_only, filter_stations_based_on_search_terms, \
    universal_search
from fastapi import Depends, HTTPException, status, APIRouter
from exceptions.custom_exceptions import StepFunctionException
from app.user_login_regisration_workflows.user_related_db_operations import UserRelatedDbOperations
from app.user_operations.vehicle_related_operations import RegisterVehicleOperations
from vendor_workflow.common_workflows import status_charging_user_common
from vendor_workflow.common_workflows.change_charger_status_common import mark_status
from data_store.data_organizer import get_data_communicator
from utility.step_function_communicator import StepFunctionCommunicator
from data_store.data_schemas import User, UserResponseModel, QrAuthStationData, BookChargerData, \
    ChargingStationLocationBasedData, ChargingStationSearchData, AllUserData, ChargingPointDataForUpdate
from app.user_login_regisration_workflows.check_current_user import get_current_active_user
from vendor_factories import read_booking_factory, read_start_charging_factory, read_stop_charging_factory, \
    read_status_charging_factory
from data_store import crud
from typing import Dict

router = APIRouter()


@router.post("/stations", response_model=UserResponseModel)
async def get_station_list(location_related_data: ChargingStationLocationBasedData,
                           current_user: User = Depends(get_current_active_user)):
    try:
        # call open search api based pass current long lat
        response = await get_stations_based_on_long_lat_only(location_related_data=location_related_data)
    except HTTPException as e:
        return {"status_code": e.status_code, "message": f"{e.detail}", "data": {}}
    else:
        return {"status_code": status.HTTP_200_OK, "message": "Fetched relevant stations nearby",
                "data": {"locations": response}}


@router.post("/search", response_model=UserResponseModel)
async def search_stations_based_on_text(location_related_data: ChargingStationLocationBasedData,
                                        search_string: str, current_user: User = Depends(get_current_active_user)):
    try:
        response = await universal_search(location_related_data, search_string=search_string)
    except HTTPException as e:
        return {"status_code": e.status_code, "message": f"{e.detail}", "data": {}}
    else:
        return {"status_code": status.HTTP_200_OK, "message": "Fetched relevant stations nearby",
                "data": {"locations": response}}


@router.post("/filter/station", response_model=UserResponseModel)
async def filter_stations_based_on_properties(location_related_data: ChargingStationLocationBasedData,
                                              filter_data: ChargingStationSearchData,
                                              current_user: User = Depends(get_current_active_user)):
    try:
        response = await filter_stations_based_on_search_terms(location_related_data, filter_data)
    except HTTPException as e:
        return {"status_code": e.status_code, "message": f"{e.detail}", "data": {}}
    else:
        return {"status_code": status.HTTP_200_OK, "message": "Fetched relevant stations nearby",
                "data": {"locations": response}}


@router.post("/auth/qr", response_model=UserResponseModel)
async def authorize_qr(station_specific_data: QrAuthStationData,
                       current_user: User = Depends(get_current_active_user), db=Depends(get_db)):
    response = crud.get_one_station_data_from_agg_table(db, station_specific_data.station_id,
                                                        station_specific_data.vendor_id)

    db_operations = UserRelatedDbOperations(db=db)
    register_vehicle = RegisterVehicleOperations(current_user=current_user,
                                                 db_operation=db_operations)
    string_list_of_vehicles = await register_vehicle.get_short_list_of_vehicles_for_current_user()

    if response:
        if response["qr_code"] == station_specific_data.qr_code:
            return {"status_code": status.HTTP_200_OK, "message": f"user is authorized to use the charging point "
                                                                  f"{station_specific_data.charger_point_id}",
                    "data": {"web_socket_url": settings.WEB_SOCKET_URL, "registered_vehicles": string_list_of_vehicles}}
        else:
            return {"status_code": status.HTTP_403_FORBIDDEN,
                    "message": f"This QR code is not authorized for station {station_specific_data.station_id}",
                    "data": {}}


@router.post("/book/charger", response_model=UserResponseModel)
async def book_specific_charger_now(book_charger_data: BookChargerData,
                                    current_user: AllUserData = Depends(get_current_active_user), db=Depends(get_db),
                                    sqs=Depends(get_sqs), step_function=Depends(get_step_function),
                                    s3_client=Depends(get_s3)):
    book_charger_data.user_id = current_user.phonenumber
    try:
        booker = read_booking_factory(vendor_id=book_charger_data.vendor_id)
        data_for_booking = await booker(book_charger_data, db, sqs, current_user, s3_client).book_charger()
    except HTTPException as e:
        return {"status_code": e.status_code,
                "message": f"{e.detail}",
                "data": {}}
    else:
        # Give the data to step function to start the state machine
        try:
            step_function_object = StepFunctionCommunicator(step_client=step_function,
                                                            data_to_parse_and_input=data_for_booking.pop(
                                                                "data_to_input_in_step_function"))
            step_function_object.start_step_function()
        except StepFunctionException as e:
            return {"status_code": e.status_code,
                    "message": f"{e.message}",
                    "data": {}}
        else:
            return {"status_code": status.HTTP_200_OK, "message": f"charging details are registered",
                    "data": data_for_booking}


@router.post("/start/charging")
async def start_charging_session(vendor_id: str, booking_id: str, start_charging_data: Dict,
                                 current_user: User = Depends(get_current_active_user),
                                 lambda_client=Depends(get_lambda), s3_client=Depends(get_s3), db=Depends(get_db),
                                 sqs=Depends(get_sqs)):
    try:
        starter = read_start_charging_factory(vendor_id=vendor_id)
        response = await starter(vendor_id=vendor_id, booking_id=booking_id,
                                 start_charging_data=start_charging_data,
                                 lambda_client=lambda_client, s3_client=s3_client, db=db, sqs=sqs).start_charging()
    except HTTPException as e:
        return {"status_code": e.status_code,
                "message": f"{e.detail}",
                "data": {}}
    else:
        return response


@router.post("/stop/charging")
async def stop_charging_session(vendor_id: str, booking_id: str, stop_charging_data: Dict,
                                current_user: User = Depends(get_current_active_user),
                                lambda_client=Depends(get_lambda), s3_client=Depends(get_s3), db=Depends(get_db),
                                sqs=Depends(get_sqs)):
    try:
        stopper = read_stop_charging_factory(vendor_id)
        response = await stopper(vendor_id=vendor_id, booking_id=booking_id,
                                 stop_charging_data=stop_charging_data,
                                 lambda_client=lambda_client, s3_client=s3_client, db=db, sqs=sqs).stop_charging()
    except HTTPException as e:
        return {"status_code": e.status_code,
                "message": f"{e.detail}",
                "data": {}}
    else:
        return response


@router.post("/internal/stop/charging")
async def stop_charging_session(vendor_id: str, booking_id: str, stop_charging_data: Dict,
                                lambda_client=Depends(get_lambda), s3_client=Depends(get_s3), db=Depends(get_db),
                                sqs=Depends(get_sqs)):
    try:
        stopper = read_stop_charging_factory(vendor_id)
        response = await stopper(vendor_id=vendor_id, booking_id=booking_id,
                                 stop_charging_data=stop_charging_data,
                                 lambda_client=lambda_client, s3_client=s3_client, db=db, sqs=sqs).stop_charging()
    except HTTPException as e:
        return {"status_code": e.status_code,
                "message": f"{e.detail}",
                "data": {}}
    else:
        return response


@router.post("/charging/status")
async def charging_session_status(vendor_id: str, booking_id: str, charging_status_data: Dict,
                                  socket_connection_id: str = None,
                                  current_user: User = Depends(get_current_active_user), db=Depends(get_db),
                                  sqs=Depends(get_sqs)):
    try:
        status_checker = status_charging_user_common.UserStatusCharging(vendor_id=vendor_id, booking_id=booking_id,
                                                                        charging_status_data=charging_status_data,
                                                                        socket_connection_id=socket_connection_id,
                                                                        db=db,
                                                                        data_communicator=get_data_communicator,
                                                                        sqs=sqs)
        response = await status_checker.provide_user_charging_status()
    except HTTPException as e:
        return {"status_code": e.status_code,
                "message": f"{e.detail}",
                "data": {}}
    else:
        return response


@router.post("/internal/charging/status")
async def charging_session_status(vendor_id: str, booking_id: str, charging_status_data: Dict,
                                  socket_connection_id: str = None,
                                  lambda_client=Depends(get_lambda), s3_client=Depends(get_s3), db=Depends(get_db),
                                  sqs=Depends(get_sqs)):
    try:
        updater = read_status_charging_factory(vendor_id)
        response = await updater(vendor_id=vendor_id, booking_id=booking_id, charging_status_data=charging_status_data,
                                 socket_connection_id=socket_connection_id, lambda_client=lambda_client,
                                 s3_client=s3_client, db=db, sqs=sqs).status_charging()
    except HTTPException as e:
        return {"status_code": e.status_code,
                "message": f"{e.detail}",
                "data": {}}
    else:
        return response


@router.post("/charger/status")
async def change_charger_status(charger_data: ChargingPointDataForUpdate, db=Depends(get_db), sqs=Depends(get_sqs)):
    try:
        status_changer = mark_status(charger_data=charger_data, db=db, sqs=sqs)
    except HTTPException as e:
        return {"status_code": e.status_code,
                "message": f"{e.detail}",
                "data": {}}
    else:
        return {"status_code": status.HTTP_200_OK,
                "message": "Charger status updated",
                "data": {}}
