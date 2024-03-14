import datetime
from data_store import data_schemas
from fastapi import HTTPException, status
from botocore.exceptions import ClientError
from utility.custom_logger import logger as logging
from .crud_data_schemas import ReadTableSchema, UpdateTableSchema, CreateEntrySchema
from utility.async_third_party_communicator import make_async_http_request
from boto3.dynamodb.conditions import Key, Attr, BeginsWith, Contains
from data_store.data_structures import ChargerStatus
from config import Settings

settings = Settings()


async def read_data_from_table(data_for_read: ReadTableSchema):
    try:
        result = await make_async_http_request(url=settings.DB_API, body=data_for_read.dict())
    except HTTPException:
        logging.exception("Error while reading data from session table")
        raise
    else:
        return result


async def update_table(data_to_update: UpdateTableSchema):
    # update to session db
    try:
        logging.debug(f"Going to update a table with data {data_to_update}")
        result = await make_async_http_request(url=settings.DB_API, body=data_to_update.dict())
    except HTTPException:
        logging.exception(f"Unable to update table for data {data_to_update.dict()}")
        raise
    else:
        return result


async def create_entry_in_table(data_to_add: CreateEntrySchema):
    try:
        logging.debug(f"Going to create a new in try using data {data_to_add}")
        result = await make_async_http_request(url=settings.DB_API, body=data_to_add.dict())
    except HTTPException:
        logging.exception(f"Unable to create a new entry for data {data_to_add.dict()}")
        raise
    else:
        return result


def get_vendor_from_db(db, vendor_id: str):
    table = db.Table("ChargingStationVendors")
    try:
        response = table.get_item(Key={"vendor_id": vendor_id})
    except ClientError:
        logging.exception("Unable to fetch data")
        return {}
    else:
        try:
            return response['Item']
        except KeyError:
            return {}


def set_vendor_transaction_id_to_db(db, vendor_id: str, reference_transaction_id):
    table = db.Table("ChargingStationVendors")
    try:
        response = table.update_item(
            Key={
                "vendor_id": vendor_id
            },
            UpdateExpression="set reference_transaction_id=:reference_transaction_id",
            ConditionExpression='attribute_exists(vendor_id)',
            ExpressionAttributeValues={
                ':reference_transaction_id': reference_transaction_id,
            },
            ReturnValues="UPDATED_NEW"
        )
    except ClientError:
        logging.exception("Hashed OTP Update failed")


def add_new_station(db, pydantic_model_station_data: data_schemas.ChargingStationStaticData):
    table = db.Table("ChargingStationStatic")
    data_to_add = dict(pydantic_model_station_data)
    table.put_item(Item=data_to_add)


def get_one_station_data(db, station_id):
    table = db.Table("ChargingStationLive")
    try:
        response = table.query(KeyConditionExpression=Key('station_id').eq(station_id))
    except ClientError as e:
        logging.error(e.response['Error']['Message'])
    else:
        return response['Items']


def get_one_station_data_from_agg_table(db, station_id: str, vendor_id: str):
    table = db.Table("ChargingStationLocation")
    try:
        response = table.query(KeyConditionExpression=Key('station_id').eq(station_id) & Key('vendor_id').eq(vendor_id))
    except ClientError as e:
        logging.error(e.response['Error']['Message'])
    else:
        return response['Items'][0]


def get_booking_details(db, booking_id: str):
    table = db.Table("ChargingSessionRecords")
    try:
        response = table.query(KeyConditionExpression=Key('booking_id').eq(booking_id))
    except ClientError as e:
        logging.error(e.response['Error']['Message'])
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unable to fetch details for the booking id {booking_id}")
    else:
        return response['Items'][0]

def add_new_entry_in_booking_table(db, charging_status_data_to_store: data_schemas.BookChargingSessionData):
    try:
        table = db.Table("ChargingSessionRecords")
        data_to_add = charging_status_data_to_store.dict()

        response = table.put_item(Item=data_to_add)
        logging.info("New data added in ChargingSessionRecords")
    except ClientError:
        logging.exception("error in adding new entry in to ChargingSessionRecords table")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to create new booking entry")
    else:
        return response


def mark_connector_status_in_agg_db_table(db, station_id, vendor_id, collective_data_to_update):
    agg_table = db.Table("ChargingStationLocation")
    expression_to_update = "set "
    values_for_update = {}
    first_join = True
    for each_element in collective_data_to_update.keys():
        if first_join:
            expression_to_update = expression_to_update + " " + f"{each_element}=:{each_element}"
            first_join = False
        else:
            expression_to_update = expression_to_update + ", " + f"{each_element}=:{each_element}"
        values_for_update.update({f":{each_element}": collective_data_to_update[each_element]})

    try:
        agg_update_response = agg_table.update_item(
            Key={
                "station_id": station_id,
                "vendor_id": vendor_id
            },
            UpdateExpression=expression_to_update,

            ConditionExpression='attribute_exists(vendor_id)',

            ExpressionAttributeValues=values_for_update,

            ReturnValues="ALL_NEW"
        )
    except ClientError as e:
        logging.exception("exception in updating data")
        return False
    else:
        return agg_update_response


def update_booking_table(db, charging_status_data_to_store: data_schemas.BookChargingSessionData):
    table = db.Table("ChargingSessionRecords")
    final_data_to_update = charging_status_data_to_store.dict(exclude_defaults=True)
    booking_id = final_data_to_update.pop("booking_id")
    vendor_id = final_data_to_update.pop("vendor_id")

    expression_to_update = "set "
    values_for_update = {}
    first_join = True
    for each_element in final_data_to_update.keys():
        if first_join:
            expression_to_update = expression_to_update + " " + f"{each_element}=:{each_element}"
            first_join = False
        else:
            expression_to_update = expression_to_update + ", " + f"{each_element}=:{each_element}"
        values_for_update.update({f":{each_element}": final_data_to_update[each_element]})

    try:
        response = table.update_item(
            Key={
                "booking_id": booking_id,
                "vendor_id": vendor_id
            },
            UpdateExpression=expression_to_update,
            ConditionExpression='attribute_exists(booking_id)',
            ExpressionAttributeValues=values_for_update,

            ReturnValues="ALL_NEW"
        )
    except ClientError as e:
        logging.exception("exception in updating data")
        return False
    else:
        return response


def update_data_in_reservation_table(db, charging_status_data_to_store: data_schemas.ReservationDataForStorage):
    table = db.Table("ReservationRegister")
    try:
        response = table.update_item(
            Key={
                "reservation_id": charging_status_data_to_store.reservation_id
            },
            UpdateExpression="set charging_status=:charging_status, charging_states=:charging_states, "
                             "energy_consumed=:energy_consumed, battery_status=:battery_status, "
                             "emission_saved=:emission_saved, total_duration=:total_duration, "
                             "total_amount=:total_amount",
            ConditionExpression='attribute_exists(reservation_id)',

            ExpressionAttributeValues={
                ':charging_status': charging_status_data_to_store.charging_status,
                ':charging_states': charging_status_data_to_store.charging_states,
                ':energy_consumed': charging_status_data_to_store.energy_consumed,
                ':battery_status': charging_status_data_to_store.battery_status,
                ':emission_saved': charging_status_data_to_store.emission_saved,
                ':total_duration': charging_status_data_to_store.total_duration_hour,
                ':total_amount': charging_status_data_to_store.estimated_cost
            },
            ReturnValues="UPDATED_NEW"
        )
        print(f"response is {response}")
    except ClientError as e:
        logging.exception("exception in updating data")
        # TODO: This needs to be removed when workflow for reservation is matured
        data_to_add = charging_status_data_to_store.dict()
        table.put_item(Item=data_to_add)
        logging.info("New data added in reservation register")
    else:
        return response


if __name__ == '__main__':
    import boto3

    db = boto3.resource('dynamodb', endpoint_url="http://172.17.0.1:8000", region_name="us-west-2")
    table = db.Table("ChargingStationLocation")

    response = table.scan()
    print(response["Items"][0])