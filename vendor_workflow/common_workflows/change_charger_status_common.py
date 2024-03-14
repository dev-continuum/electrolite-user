from data_store import data_schemas, data_structures, crud
from pydantic import BaseModel
from fastapi import status, HTTPException
from utility.custom_logger import logger
import simplejson


def mark_status(charger_data: data_schemas.ChargingPointDataForUpdate, sqs, db):
    one_station_data = crud.get_one_station_data_from_agg_table(station_id=charger_data.station_id,
                                                                vendor_id=charger_data.vendor_id, db=db)
    # get all live chargers
    total_charger_data = one_station_data["total_charger_data"]
    expanded_total_charger_data = one_station_data["expanded_total_charger_data"]

    for charger in total_charger_data:
        if charger["charger_point_id"] == charger_data.charger_point_id:
            charger["charger_point_status"] = charger_data.charger_point_status
            for connector in charger["connectors"]:
                if connector["connector_point_id"] == charger_data.connector_point_id:
                    connector["status"] = charger_data.connector_point_status

    for charger in expanded_total_charger_data:
        if charger["charger_point_id"] == charger_data.charger_point_id and charger["connector_point_id"] == charger_data.connector_point_id:
            charger["charger_point_status"] = charger_data.charger_point_status

    logger.debug(f"Here is the final data to update in DB {total_charger_data}")

    response = crud.mark_connector_status_in_agg_db_table(db=db, station_id=charger_data.station_id,
                                                          vendor_id=charger_data.vendor_id,
                                                          collective_data_to_update={"total_charger_data":
                                                                                         total_charger_data,
                                                                                     "expanded_total_charger_data": expanded_total_charger_data})

    if response:
        data_to_send_to_sqs = simplejson.dumps(
            data_schemas.ChargingStationStaticData.parse_obj(response['Attributes']).dict())
        logger.info(f"send this response to the sqs {data_to_send_to_sqs}")
        # send to sqs for updating it in search indexing
        response = sqs.send_message(
            QueueUrl="https://sqs.ap-south-1.amazonaws.com/683563489644/LocationDataQueue",
            MessageBody=data_to_send_to_sqs)
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            logger.debug(f"Sent data successfully on sqs {data_to_send_to_sqs}")
            # TODO: optimize the response
            return True
        else:
            raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED, detail="Unable to send data to sqs for the opensearch update")