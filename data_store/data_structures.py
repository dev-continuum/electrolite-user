from enum import Enum


class ChargingStatus(Enum):
    BOOKED = 'Session is booked but not started.'
    STARTED = 'Booked session started successfully'
    START_FAILED = "Fail to start charging"
    REBOOKED = "User booked the same charger again"
    IN_PROGRESS = 'Charging session is in progress.'
    PROGRESS_UPDATE_UNKNOWN = 'Unable to get update'
    USER_STOPPED = 'User stopped the session in between'
    COMPLETED = 'Charging session completed successfully'
    TERMINATED = 'Terminated from server side'
    UNKNOWN_ERROR = 'Some case which is not handled in any scenario'
    STOP_FAILED = 'Stop initiated but failed'


class ChargerStatus(Enum):
    CHARGER_AVAILABLE = "AVAILABLE"
    CHARGER_BUSY = "BUSY"
    CHARGER_NOT_WORKING = "FAULTY"
    CHARGER_BOOKED = "BOOKED"
    CHARGER_RESERVED = "RESERVED"


class ChargingCalculationMode(Enum):
    TIME_BASED_CALCULATION = "TIME"
    ENERGY_BASED_CALCULATION = "ENERGY"


class Ratings(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
