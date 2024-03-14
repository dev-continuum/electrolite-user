import boto3
from ..app import get_db


def create_user_table(dynamodb=None):
    dynamodb = get_db()
    table = dynamodb.create_table(
        TableName='users',
        KeySchema=[
            {
                'AttributeName': 'email',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'username',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                "AttributeName": "hashed_password",
                "AttributeType": "S"
            },
            {
                "AttributeName": "is_active",
                "AttributeType": "BOOL"
            },
            {
                "AttributeName": "vehicle_model",
                "AttributeType": "S"
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table


