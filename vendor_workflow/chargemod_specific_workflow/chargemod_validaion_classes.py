from pydantic import BaseModel
from typing import Optional


class ChargeModHeader(BaseModel):
    Accept: str
    key: str
    Authorization: str

    class Config:
        use_enum_values = True


class ChargeModStartChargeParams(BaseModel):
    station_id: str
    reference_transaction_id: str
    user_id: str
    relay_switch_number: str
    max_energy_consumption: Optional[str] = 10
    name: Optional[str] = None
    model: Optional[str] = None
    rate: Optional[str] = None
    image: Optional[str] = None
    timings: Optional[str] = None
    sockets: Optional[str] = None
    vehicle_types: Optional[str] = None
    address: Optional[str] = None


class ChargeModStopChargeParams(BaseModel):
    reference_transaction_id: str
    id: Optional[str] = None
    name: Optional[str] = None
    model: Optional[str] = None
    rate: Optional[str] = None
    image: Optional[str] = None
    timings: Optional[str] = None
    sockets: Optional[str] = None
    vehicle_types: Optional[str] = None
    address: Optional[str] = None


class ChargeModChargeActivityParams(BaseModel):
    id: str
