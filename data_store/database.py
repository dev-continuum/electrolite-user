from utility.custom_logger import logger as logging
from app import get_db

"""
S – String
N – Number
B – Binary
BOOL – Boolean
NULL – Null
M – Map
L – List
SS – String Set
NS – Number Set
BS – Binary Set
"""


def check_table_preexist(db, table_name: str):
    try:
        db.Table(table_name).key_schema
    except Exception:
        return False
    else:
        return True


def create_user_table(db):
    dynamo_db = db
    if not check_table_preexist(db, table_name='User'):
        logging.info("Creating new User table")
        table = dynamo_db.create_table(
            TableName='User',
            KeySchema=[
                {
                    'AttributeName': 'phonenumber',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'phonenumber',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )


def create_live_station_table(db):
    dynamo_db = db
    if not check_table_preexist(db, table_name='ChargingStationLive'):
        logging.info("Creating new Live station table")
        table = dynamo_db.create_table(
            TableName='ChargingStationLive',
            KeySchema=[
                {
                    'AttributeName': 'station_id',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'evse_id',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            LocalSecondaryIndexes=[
                {
                    'IndexName': "RESERVATIONS_INDEX",
                    'KeySchema': [
                        {
                            'KeyType': 'HASH',
                            'AttributeName': 'station_id'
                        },
                        {
                            'KeyType': 'RANGE',
                            'AttributeName': 'evse_status'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    }

                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'station_id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'evse_id',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'evse_status',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )


def create_static_station_table(db):
    dynamo_db = db
    if not check_table_preexist(db, table_name='ChargingStationStatic'):
        logging.info("Creating new Static station data table")
        table = dynamo_db.create_table(
            TableName='ChargingStationStatic',
            KeySchema=[
                {
                    'AttributeName': 'station_id',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'station_id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )


def create_reservation_register_table(db):
    dynamo_db = db
    if not check_table_preexist(db, table_name='ReservationRegister'):
        logging.info("Creating new Reservation register table")
        table = dynamo_db.create_table(
            TableName='ReservationRegister',
            KeySchema=[
                {
                    'AttributeName': 'reservation_id',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'reservation_id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )


def create_booking_session_table(db):
    dynamo_db = db
    if not check_table_preexist(db, table_name='ChargingSessionRecords'):
        logging.info("Creating new ChargingSessionRecords table")
        table = dynamo_db.create_table(
            TableName='ChargingSessionRecords',
            KeySchema=[
                {
                    'AttributeName': 'booking_id',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'vendor_id',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'booking_id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'vendor_id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )


def create_tables():
    db = get_db()
    create_user_table(db)
    create_live_station_table(db)
    create_static_station_table(db)
    create_reservation_register_table(db)
    create_booking_session_table(db)

