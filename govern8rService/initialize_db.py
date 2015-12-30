from __future__ import print_function # Python 2/3 compatibility
import boto3
import botocore
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://localhost:8000")
try:
    account_table = dynamodb.Table('Account')
    print(account_table.table_status)
except botocore.exceptions.ClientError as e:
    print(e.response['Error']['Code'])

try:
    account_table = dynamodb.create_table(
        TableName='Account',
        KeySchema=[
            {
                'AttributeName': 'public_key',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'public_key',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    print("Account Table status:", account_table.table_status)
except botocore.exceptions.ClientError as e:
    print(e.response['Error']['Code'])
    account_table = dynamodb.Table('Account')
    response = account_table.query(KeyConditionExpression=Key('public_key').eq("0420f91a997d0348b7a90e87552cd1b954020db6f159507c28b610ef6a7a871bbcc52c84cd9ae3ff54fdd3c9a8b3b2794f9f8272ea7935eac9370991be4984c275"))
    items = response['Items']
    account_table.delete()


try:
    notarization_table = dynamodb.create_table(
        TableName='Notarization',
        KeySchema=[
            {
                'AttributeName': 'digest',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'digest',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }


    )
    print("Notarization Table status:", notarization_table.table_status)
except botocore.exceptions.ClientError as e:
    print(e.response['Error']['Code'])
    # account_table = dynamodb.Table('Notarization')
    # account_table.delete()
