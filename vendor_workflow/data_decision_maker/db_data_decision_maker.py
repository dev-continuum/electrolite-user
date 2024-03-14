from utility.custom_logger import logger
from fastapi import status
from data_store.data_structures import ChargingStatus


def return_start_success_data(response_data):
    return {"start_time": response_data["start_time"], "start_charging_status": True,
            "current_status": ChargingStatus.STARTED.name,
            "charging_activity_id": response_data.get("charging_activity_id", None)}


def return_start_error_data(response_data=None):
    return {"start_charging_status": False, "stop_charging_status": False,
            "current_status": ChargingStatus.START_FAILED.name}


def return_stop_success_data(response_data):
    return {
        "current_status": ChargingStatus.COMPLETED.name,
        "stop_charging_status": True,
        "user_stopped": True
    }


def return_stop_failure_data(response_data):
    return {"stop_charging_status": False, "current_status": ChargingStatus.STOP_FAILED.name,
            "user_stopped": True}


def return_status_success_data(response_data):
    return {
            "current_energy_consumed": response_data.get("current_energy_consumed", None),
            "meter_values": response_data.get("meter_values", None),
            "emission_saved": response_data.get("emission_saved", None),
            "battery_status": response_data.get("battery_status", None),
            "current_range": response_data.get("current_range", None)
            }

def return_status_error_data(response_data):
    return {"current_status": ChargingStatus.PROGRESS_UPDATE_UNKNOWN.name}


def response_mapper(action, action_type, response_data=None):
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
    return response_mapper_result(response_data)


class DbUpdateDecisionMaker:
    def __init__(self, response, charging_data_update_for_session, action):
        self.response_data = response
        self.charging_data_update_for_session = charging_data_update_for_session
        self.response_decision_maker = {status.HTTP_500_INTERNAL_SERVER_ERROR: self.prepare_data_for_error,
                                        status.HTTP_503_SERVICE_UNAVAILABLE: self.prepare_data_for_error,
                                        status.HTTP_200_OK: self.prepare_data_for_success}
        self.action = action

    def decide(self):
        return self.response_decision_maker[self.response_data["status_code"]]()

    def prepare_data_for_error(self):
        error_data = response_mapper(action=self.action, action_type="error", response_data=self.response_data)
        return self._prepare_data_for_session_db_update(error_data)

    def prepare_data_for_success(self):
        logger.info(f"Preparing DB update for success. Action: {self.action}")
        success_data = response_mapper(action=self.action, action_type="success",
                                       response_data=self.response_data)
        return self._prepare_data_for_session_db_update(success_data)

    def _prepare_data_for_session_db_update(self, data_to_update):
        temp_data = self.charging_data_update_for_session.copy()
        temp_data.update(data_to_update)
        return temp_data
