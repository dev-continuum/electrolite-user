from data_store import data_schemas
from utility.custom_logger import logger
from fastapi import status, HTTPException
from app.user_login_regisration_workflows.user_related_db_operations import UserRelatedDbOperations
from botocore.client import ClientError


class RateStations:
    def __init__(self, current_user, db_operations):
        self.current_user = current_user
        self.db_operations: UserRelatedDbOperations = db_operations

    def add_rating_for_a_station(self, station_rating_data: data_schemas.RatingStationData):
        # TODO: Add a background task for avg rating calculation
        table = self.db_operations.db.Table("ChargingStationLocation")
        try:
            response = table.update_item(
                Key={
                    "station_id": station_rating_data.station_id,
                    "vendor_id": station_rating_data.vendor_id
                },
                ExpressionAttributeNames={"#rating": "rating",
                                          "#key1": f"{station_rating_data.rating}"},
                ExpressionAttributeValues={
                    ':count': 1,
                },
                ConditionExpression='attribute_exists(#rating.avg_rating)',
                UpdateExpression="set #rating.#key1 = #rating.#key1 + :count",
                ReturnValues="UPDATED_NEW"
            )
        except ClientError:
            logger.exception("Unable to update rating data")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Rating update failed due to unknown params")
        else:
            return {"status_code": status.HTTP_200_OK, "message": f"rating_data_updated for the station {station_rating_data.station_id}",
                    "data": {}}
