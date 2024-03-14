from utility.custom_logger import logger
from fastapi import status
from data_store.data_structures import ChargingStatus


def return_start_success_data(primary_data_to_send):
    return {"status_code": status.HTTP_200_OK, "message": f"Charging started",
            "data": primary_data_to_send}


def return_start_error_data(primary_data_to_send):
    return {"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"Charging start failed",
            "data": primary_data_to_send}


def return_stop_success_data(primary_data_to_send):
    return {"status_code": status.HTTP_200_OK, "message": f"Charging stopped", "data": primary_data_to_send}


def return_stop_failure_data(primary_data_to_send):
    return {"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": f"Charging stop failed",
            "data": primary_data_to_send}


def return_status_success_data(primary_data_to_send):
    return {"status_code": status.HTTP_200_OK, "message": f"Current charging status",
            "data": primary_data_to_send}


def return_status_error_data(primary_data_to_send):
    return {"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR, "message": f"Charging status not available",
            "data": primary_data_to_send}


def response_mapper(action, action_type, primary_data_to_send: dict = None, secondary_data_to_update: dict = None):
    if secondary_data_to_update:
        primary_data_to_send.update(secondary_data_to_update)
        logger.debug(f"There was a secondary data. Updated data is {primary_data_to_send}")
    action_data_map = {
        "start": {
            "error": return_start_error_data,
            "success": return_start_success_data
        },
        "stop": {
            "error": return_stop_failure_data,
            "success": return_stop_success_data
        },

        "status": {
            "error": return_status_error_data,
            "success": return_status_success_data
        }
    }
    response_mapper_result = action_data_map[action][action_type]
    logger.info(f"Result from response mapper is {response_mapper_result}")
    return response_mapper_result(primary_data_to_send)


class UserDataDecisionMaker:
    def __init__(self, response, updated_session_db_data, action, charging_data=None):
        self.action = action
        self.response = response
        self.updated_session_db_data = updated_session_db_data
        self.charging_data = charging_data
        self.user_response_decision_maker = {
            status.HTTP_500_INTERNAL_SERVER_ERROR: self.prepare_internal_error_data,
            status.HTTP_503_SERVICE_UNAVAILABLE: self.prepare_service_unavailable_error,
            status.HTTP_200_OK: self.prepare_success_data}

    def decide(self):
        return self.user_response_decision_maker[self.response["status_code"]]()

    def prepare_internal_error_data(self):
        return response_mapper(action=self.action, action_type="error",
                               primary_data_to_send=self.updated_session_db_data)

    def prepare_service_unavailable_error(self):
        return response_mapper(action=self.action, action_type="error",
                               primary_data_to_send=self.updated_session_db_data)

    def prepare_success_data(self):
        logger.info(f"Preparing User update for success. Action: {self.action}")
        return response_mapper(action=self.action, action_type="success",
                               primary_data_to_send=self.updated_session_db_data,
                               secondary_data_to_update={"data_to_stop": self.charging_data})
