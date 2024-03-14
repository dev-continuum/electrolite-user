import datetime
from enum import Enum
from fastapi import HTTPException, status
from pydantic import BaseModel, AnyHttpUrl, validator
from typing import Optional, Dict, List
from decimal import Decimal
from data_store.data_structures import ChargingStatus, ChargingCalculationMode, ChargerStatus, Ratings
import pytz


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class InitUser(BaseModel):
    phonenumber: str
    hashed_otp: str
    otp: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
    registration_number: Optional[str] = None
    user_bookings: Optional[Dict] = {}
    vehicle_data: Optional[List] = []
    ongoing_charging: Optional[Dict] = {}
    provider: Optional[str] = None
    wallet: Optional[int] = 0
    profile_pic: Optional[AnyHttpUrl] = None
    address: Optional[str] = None

    class Config:
        orm_mode = True


class InitSocialUser(InitUser):
    hashed_otp: Optional[str] = ""


class SocialMediaSignupData(BaseModel):
    id: str
    email: str
    display_name: str
    provider: str
    agree_terms: bool


class FirstTimeUser(BaseModel):
    phonenumber: str
    agree_terms: bool

    class Config:
        orm_mode = True


class AllUserData(BaseModel):
    phonenumber: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
    vehicle_data: Optional[List] = None
    registration_number: Optional[str] = None
    user_bookings: Optional[Dict] = {}
    ongoing_charging: Optional[Dict] = {}
    wallet: Optional[int] = 0
    profile_pic: Optional[AnyHttpUrl] = None
    address: Optional[str] = None

    class Config:
        orm_mode = True


class User(BaseModel):
    phonenumber: str

    class Config:
        orm_mode = True


class UserToken(User):
    otp: Optional[str] = None


class UserInDB(User):
    hashed_otp: str


class RegisteredUser(BaseModel):
    first_name: str
    last_name: str
    email: str


class UpdateProfileData(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None


class RegisterNewVehicle(BaseModel):
    vehicle_type: str
    make: str
    model: str
    registration_number: str
    connector_type: str
    # these two attributes will come from vehicle not sure how to get it currently
    current_distance_range: Optional[str] = '20'
    distance_unit: Optional[str] = "km"
    current_charge_available: Optional[int] = 20
    current_charge_available_unit: Optional[str] = "%"

    power_capacity: Optional[str] = None
    power_capacity_unit: Optional[str] = "Kwh"
    range: Optional[str] = None
    max_speed: Optional[str] = None
    electric_energy_consumption: Optional[str] = None
    battery_technology: Optional[str] = None
    battery_density: Optional[str] = None
    battery_cycle: Optional[str] = None




class ChargingStationLiveData(BaseModel):
    station_id: str
    evse_id: int
    evse_status: str
    connector_id: str
    connector_status: str

    class Config:
        orm_mode = True


class ChargingStationLocationBasedData(BaseModel):
    long: float
    lat: float
    country: Optional[str] = "IN"
    proximity_in_km: Optional[int] = 10
    limit: Optional[int] = 20
    offset: Optional[int] = 0


class ChargingStationSearchData(BaseModel):
    text: Optional[str] = "null"
    pincode: Optional[str] = "null"
    distance: Optional[int] = 0
    area: Optional[str] = "null"
    country: Optional[str] = "null"
    state: Optional[str] = "null"
    city: Optional[str] = "null"
    name: Optional[str] = "null"
    charger_point_type: Optional[str] = "null"
    power_capacity: Optional[str] = "null"
    auto_service: Optional[str] = "null"
    food_court: Optional[str] = "null"
    cctv: Optional[str] = "null"
    chemist_shop: Optional[str] = "null"
    connector_status: Optional[str] = "null"
    avg_rating: Optional[float] = 0.0


class ChargingPointDataForUpdate(BaseModel):
    station_id: str
    vendor_id: str
    charger_point_id: int
    charger_point_status: ChargerStatus
    connector_point_id: int
    connector_point_status: ChargerStatus

    class Config:
        use_enum_values = True


class ChargingStationStaticData(BaseModel):
    station_id: str
    vendor_id: str
    name: str
    address_line: str
    town: str
    state: str
    postal_code: str
    latitude: Decimal
    longitude: Decimal
    country: str
    qr_code: Optional[str] = None
    total_connectors_available: int
    station_status: str
    station_time: Optional[Dict] = None
    distance_unit: Optional[int] = None
    is_ocpp: Optional[bool] = False
    total_charger_data: List
    expanded_total_charger_data: List
    image: Optional[AnyHttpUrl] = None
    geo_address: List
    uid: Optional[str] = None,
    rating: Dict = {"avg_rating": 0,
                    "5": 0,
                    "4": 0,
                    "3": 0,
                    "2": 0,
                    "1": 0,
                    }

    class Config:
        orm_mode = True
        use_enum_values = True


class QrAuthStationData(BaseModel):
    station_id: str
    vendor_id: str
    charger_point_id: int
    connector_point_id: int
    qr_code: str


class RatingStationData(BaseModel):
    station_id: str
    vendor_id: str
    rating: Ratings

    class Config:
        use_enum_values = True


class ReservationData(BaseModel):
    station_id: str
    evse_id: Optional[int] = None
    connector_id: Optional[int] = None
    date: datetime.date
    from_time: datetime.time
    # to_date: datetime.date
    to_time: datetime.time
    # hour: Optional[datetime.timedelta] = None
    # minute: Optional[datetime.timedelta] = None
    # seconds: Optional[float] = None


class ReservationDataDuration(BaseModel):
    station_id: str
    charger_point_id: int = None
    connector_point_id: int = None
    # TODO: Dummy Alert: Assigning static data here change later
    date: datetime.date
    from_time: datetime.time
    hour: float
    minute: float
    ampm: str


class ReservationDataReschedule(BaseModel):
    date: datetime.date
    from_time: datetime.time
    hour: float
    minute: float
    ampm: str


class ReservationCancel(BaseModel):
    user_id: str
    station_id: str
    charger_point_id: int = None
    connector_point_id: int = None
    date: datetime.date
    start_time: datetime.time
    reservation_id: Optional[str] = None


class ReservationDataDurationInternal(BaseModel):
    station_id: str
    charger_point_id: int = None
    connector_point_id: int = None
    # TODO: Dummy Alert: Assigning static data here change later
    evse_id: Optional[int] = None
    connector_id: Optional[int] = None
    date: datetime.date
    from_time: datetime.time
    from_time_localized: Optional[datetime.time] = None
    to_time: Optional[datetime.time] = None
    to_time_localized: Optional[datetime.time] = None
    hour: Optional[float] = None
    minute: Optional[float] = None
    ampm: Optional[str] = None


class ReservationDataForConflictCheck(BaseModel):
    station_id: str
    charger_point_id: int = None
    connector_point_id: int = None
    date: datetime.date
    from_time: datetime.time
    to_time: datetime.time


class ReservationDataForStorage(BaseModel):
    reservation_time: str
    reservation_id: str
    user_id: Optional[str] = None
    station_id: Optional[str] = None
    charger_point_id: Optional[int] = None
    connector_point_id: Optional[int] = None
    charging_status: Optional[str] = ""
    payment_mode: Optional[str]
    vehicle_used: Optional[str]
    charging_states: Optional[Dict] = {}
    energy_consumed: Optional[Decimal]
    battery_status: Optional[int]
    emission_saved: Optional[Decimal]

    date: Optional[str]
    from_time: Optional[str] = None
    to_time: Optional[str] = None
    total_duration_hour: Optional[Decimal]
    charging_timer: Optional[datetime.datetime] = None

    estimated_cost: Optional[Decimal] = Decimal(0.0)
    station_name: Optional[str] = None
    station_address: Optional[str] = None
    charger_type: Optional[str] = None
    otp: Optional[int] = None


class BookChargerData(BaseModel):
    user_id: Optional[str]
    station_id: str
    vendor_id: str
    charger_point_id: int
    connector_point_id: int
    socket_connection_id: Optional[str] = None
    charger_point_type: str
    calculation_method: ChargingCalculationMode
    target_duration_timestamp: Optional[str] = None
    target_energy_kw: Optional[float] = None
    currency_unit: Optional[str] = "INR"
    vehicle_used: Optional[str]

    @validator('target_duration_timestamp')
    def convert_string_to_time_stamp(cls, v):
        if v:
            v = v.lower()
            if 'min' in v.lower():
                return f"00:{v.split('m')[0].strip()}:00"
            elif 'hr' in v.lower():
                print(v.split('h')[0].strip())
                return f"{v.split('h')[0].strip()}:00:00"
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Provide duration unit either in minute or hour")


class DataToGenerateForBookingSession(BookChargerData):
    booking_id: str
    booking_time: str
    date: str
    time_zone: str
    estimated_cost: Decimal
    tariff_applied: Decimal
    current_status: Optional[ChargingStatus] = ChargingStatus.BOOKED.name
    # details below can be vendor specific hence may or may not be needed
    reference_transaction_id: Optional[int]
    vendor_user_id: Optional[int]
    charger_status: Optional[str]
    payment_mode: Optional[str] = "wallet"
    station_name: Optional[str] = ""
    charger_point_type: Optional[str] = ""
    station_address: Optional[str] = ""
    avg_rating: Optional[str]


class BookChargingSessionData(BaseModel):
    # static data need to be inserted one time
    booking_time: Optional[str] = ""
    booking_id: str
    vendor_id: str
    socket_connection_id: Optional[str]
    date: Optional[str]
    calculation_method: Optional[ChargingCalculationMode] = None
    reference_transaction_id: Optional[int] = None
    vendor_user_id: Optional[int] = None
    user_id: Optional[str] = None
    station_id: Optional[str] = None
    charger_point_id: Optional[int] = None
    connector_point_id: Optional[int] = None
    charger_point_type: Optional[str] = None
    avg_rating: Optional[str] = None
    charging_activity_id: Optional[int] = None
    charger_status: Optional[str] = ""
    payment_mode: Optional[str] = ""
    vehicle_used: Optional[str] = ""
    expanded_vehicle_data: Optional[Dict] = {}
    target_duration_timestamp: Optional[str] = None
    target_energy_kw: Optional[Decimal] = Decimal(0.0)
    initial_estimated_cost: Optional[Decimal] = Decimal(0.0)
    estimated_cost_after_offer: Optional[Decimal] = Decimal(0.0)
    estimated_cost: Optional[Decimal] = Decimal(0.0)
    wallet_recharge: Optional[dict] = None
    tariff_applied: Optional[Decimal] = Decimal(0.0)
    offer_applied: Optional[str] = None
    gst: Optional[str] = None
    station_name: Optional[str] = None
    station_address: Optional[str] = None
    otp: Optional[int] = None

    # Dynamic data fields needs update during session
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    time_zone: Optional[str] = None
    start_charging_status: Optional[bool] = False
    battery_status: Optional[int]
    current_range: Optional[str] = None
    emission_saved: Optional[Decimal]
    current_status: Optional[str] = ""
    meter_values: Optional[Dict] = None
    charging_states: Optional[Dict] = {}
    readable_summary: Optional[Dict] = {}
    relay_switch_number: Optional[int] = None

    # these two are very important for billing needs to updated wherever possible
    current_energy_consumed: Optional[Decimal] = Decimal(0.0)
    current_charging_timer: Optional[str] = None

    # Final calculations needed after session is ended
    final_duration_timestamp: Optional[str] = None
    final_energy_consumed: Optional[Decimal] = Decimal(0.0)
    final_cost: Optional[Decimal] = Decimal(0.0)
    stop_charging_status: Optional[bool] = False
    user_stopped: Optional[bool] = False
    charging_target_reached: Optional[bool] = False
    data_to_stop: Optional[Dict] = None

    class Config:
        use_enum_values = True


class ReservationDataToStations(BaseModel):
    station_id: str
    evse_id: int
    connector_id: int
    user_id: str
    date: str
    duration_delta: datetime.timedelta
    from_time: str


class DataToScheduleReservation(BaseModel):
    station_id: str
    evse_id: int
    connector_id: int
    user_id: str
    expiry_date_time: str
    from_time: str


class UserBookings(User):
    user_bookings: List = []


class UserResponseModel(BaseModel):
    status_code: int
    message: str
    data: Dict


class TokenResponseModel(UserResponseModel):
    access_token: Optional[str]
    token_type: str = "bearer"


class FilterData(BaseModel):
    latitude: Decimal
    longitude: Decimal
    distance: int
    connector_type: str
    amenities: Optional[str] = None
    available_stations: Optional[bool] = True


class SearchStation(BaseModel):
    latitude: Decimal
    longitude: Decimal
    station_keyword: str


class OrderDataSchemaToSend(BaseModel):
    user_id: Optional[str] = None
    amount: int
    currency: Optional[str] = "INR"
    receipt: Optional[str] = "test"
    notes: Optional[dict] = {}


class TotalDataForTransactionUpdate(BaseModel):
    user_id: Optional[str] = None
    amount: int
    add: bool
    deduct: bool
    razorpay_init_order_id: str
    razorpay_payment_id: Optional[str]
    razorpay_order_id: Optional[str]
    razorpay_signature: Optional[str]