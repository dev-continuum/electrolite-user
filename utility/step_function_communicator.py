import simplejson
from config import Settings
from pydantic import BaseModel
from fastapi import status
from typing import Optional, Dict
from decimal import Decimal
import datetime
import uuid
from utility.custom_logger import logger as logging
from exceptions.custom_exceptions import StepFunctionException
settings = Settings()


class InputDataToStepFunction(BaseModel):
    booking_id: str
    station_id: str
    vendor_id: str
    charger_point_id: int
    connector_point_id: int
    target_duration_timestamp: Optional[str] = None
    target_energy_kw: Optional[Decimal] = None
    expanded_vehicle_data: Optional[Dict] = {}
    start_time: Optional[str] = None


class StepFunctionCommunicator:
    def __init__(self, step_client, data_to_parse_and_input):
        self.input_data = data_to_parse_and_input
        self.step_client = step_client

    def parse_data_for_input(self):
        parsed_data = InputDataToStepFunction.parse_obj(self.input_data)
        # return json encoded data to send it to step function
        logging.debug(f"Data for step function is parsed {parsed_data}")
        final_data = {"wait_time": settings.STEP_FUNCTION_FREQ_IN_SEC, "data_for_lambda": parsed_data.dict()}
        return simplejson.dumps(final_data,  use_decimal=True)

    def start_step_function(self):
        try:
            result = self.step_client.start_execution(
                stateMachineArn=settings.STEP_FUNCTION_ARN,
                name=f"user_service_{uuid.uuid4()}",
                input=self.parse_data_for_input())
        except Exception as e:
            logging.exception("Error in starting tep function")
            raise StepFunctionException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, message="Unable to start session monitoring service")
        else:
            logging.info(f"Step function started for booking id {self.input_data['booking_id']}")
            return result

