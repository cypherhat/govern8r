import requests
import boto3
import botocore
from blockcypher import embed_data, get_transaction_details
from boto3.dynamodb.conditions import Key
import hashlib
from datetime import datetime
import configuration
config = configuration.NotaryConfiguration()
blockcypher_token = config.get_block_cypher_token()


coin_network = 'btc'
if config.get_test_mode():
    coin_network = 'btc-testnet'


def add_to_blockchain(data_value):
    try:
        response = embed_data(to_embed=data_value, api_key=blockcypher_token, data_is_hex=True,
                              coin_symbol=coin_network)
        transaction_hash = response['hash']
        return transaction_hash
    except requests.ConnectionError as e:
        print e
        return None


def check_notarization(notarization):
    if (notarization is None) or \
            (not notarization['document_hash']) or \
            (not notarization['notary_hash']) or \
            (not notarization['address']) or \
            (not notarization['date_created']) or \
            (not notarization['transaction_hash']):
        return False
    else:
        return True


class NotarizationService(object):
    def __init__(self, wallet):
        self.wallet = wallet
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url=config.get_db_url())
        try:
            self.notarization_table = self.dynamodb.Table('Notarization')
            print("Notarization Table is %s" % self.notarization_table.table_status)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                self.create_notarization_table()

    def create_notarization_table(self):
        try:
            self.notarization_table = self.dynamodb.create_table(
                    TableName='Notarization',
                    KeySchema=[
                        {
                            'AttributeName': 'document_hash',
                            'KeyType': 'HASH'
                        }
                    ],
                    AttributeDefinitions=[
                        {
                            'AttributeName': 'document_hash',
                            'AttributeType': 'S'
                        }
                    ],
                    ProvisionedThroughput={
                        'ReadCapacityUnits': 10,
                        'WriteCapacityUnits': 10
                    }
            )
            print("Notarization Table is %s" % self.notarization_table.table_status)
        except botocore.exceptions.ClientError as e:
            print(e.response['Error']['Code'])

    def sign_and_hash(self, document_hash):
        signature = self.wallet.sign(document_hash)
        hashed_signature = hashlib.sha256(signature).digest()
        hashed_document_hash = hashlib.sha256(document_hash).digest()
        notary_hash = hashlib.sha256(hashed_signature + hashed_document_hash).digest()
        return notary_hash

    def notarize(self, notarization):
        notary_hash = self.sign_and_hash(notarization['document_hash'])
        hex_hash = str(notary_hash).encode("hex")
        notarization['notary_hash'] = hex_hash
        transaction_hash = add_to_blockchain(hex_hash)
        if transaction_hash is not None:
            notarization['transaction_hash'] = transaction_hash
            notarization['date_created'] = datetime.now().isoformat(' ')
            if self.create_notarization(notarization):
                return notarization

        return None

    def create_notarization(self, notarization):
        if not check_notarization(notarization):
            return None
        try:
            print "Notarization is "
            print notarization
            self.notarization_table.put_item(Item=notarization)
        except botocore.exceptions.ClientError as e:
            print(e.response['Error']['Code'])
            return False

        return True

    def get_notarization_by_document_hash(self, document_hash):
        response = self.notarization_table.query(KeyConditionExpression=Key('document_hash').eq(document_hash))

        if len(response['Items']) == 0:
            return None
        else:
            return response['Items'][0]

    def get_notarization_status(self, document_hash):
        notarization_data = self.get_notarization_by_document_hash(document_hash)
        status_data = get_transaction_details(notarization_data['transaction_hash'], coin_network)
        if status_data is None:
            return None
        else:
            return status_data
