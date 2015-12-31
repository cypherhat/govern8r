from __future__ import print_function # Python 2/3 compatibility
import boto3
import botocore
from boto3.dynamodb.conditions import Key
from bitcoinlib.signmessage import VerifyMessage, BitcoinMessage
from bitcoinlib.wallet import P2PKHBitcoinAddress
from datetime import datetime
import hashlib
import os
import random
import time
from bitcoinlib.core.key import CPubKey


def to_bytes(x): return x if bytes == str else x.encode()

i2b = chr if bytes == str else lambda x: bytes([x])
b2i = ord if bytes == str else lambda x: x
NONCE_LEN = 16
# Expiration delay (in seconds)
EXPIRATION_DELAY = 600


class AccountDbService(object):

    def __init__(self):
        # Initializes some dictionaries to store accounts
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://localhost:8000")
        try:
            self.account_table = self.dynamodb.Table('Account')
            print(self.account_table.table_status)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                self.create_account_table()

    def has_expired(self):
        '''
        Checks if nonce has expired
        '''
        delta = datetime.now() - self.created
        return delta.total_seconds() > Nonce.EXPIRATION_DELAY

    def generate_nonce(self):
        '''
        Generates a random nonce
        Inspired from random_key() in https://github.com/vbuterin/pybitcointools/blob/master/bitcoin/main.py
        Credits to https://github.com/vbuterin
        '''
        entropy = str(os.urandom(32)) + str(random.randrange(2**256)) + str(int(time.time())**7)
        return hashlib.sha256(to_bytes(entropy)).hexdigest()[:NONCE_LEN]

    def create_account_table(self):
        try:
            self.account_table = self.dynamodb.create_table(
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

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ResourceInUseException':
                print("Houston, we have a problem: the Account Table exists.")
    
    def create_account(self, account):
        '''
        Create a account entry in db
        Parameters:
            account = Account object to store in db
        '''
        # Checks parameter
        if not self._check_account(account):
            return False
        # Checks that a account with same values has not already been stored in db
        client_public_key = account['public_key']
        decoded = client_public_key.decode("hex")
        pubkey = CPubKey(decoded)
        rawaddress = P2PKHBitcoinAddress.from_pubkey(pubkey)
        address = str(rawaddress)

        if self.get_account_by_address(address) is None:
            # Creates the account in db
            signature = account['signature']
            message = BitcoinMessage(account['email'])
            if VerifyMessage(address, message, signature):
                account['nonce'] = self.generate_nonce()
                account['created'] = datetime.now().isoformat(' ')
                account['status'] = 'PENDING'
                account['address'] = str(address)
                self.account_table.put_item(Item=account)
                return True
            else:
                return False
        else:
            return False         

    def update_account(self, account):
        '''
        Update a account entry in db
        Parameters:
            account = Account object to update in db
        '''
        # Checks parameter
        if not self._check_account(account):
            return False
        # Checks that a account with same values exists in db
        if not self.get_account_by_public_key(account.public_key) is None:
            # Updates the account in db
            return True
        else:
            return False        
    
    def delete_account(self, account):
        '''
        Delete a account entry from db
        Parameters:
            account = Account object to delete
        '''
        # Checks parameter
        if account is None: return False
        # Checks that a account with same values exists in db
        if not self.get_account_by_public_key(account.public_key) is None:
            return True
        else:
            return False        
    
    def get_account_by_public_key(self, public_key):
        '''
        Gets a account associated to a given account id
        Parameters:
            public_key = account id
        '''
        response = self.account_table.query(KeyConditionExpression=Key('public_key').eq(public_key))

        if len(response['Items']) == 0:
            return None
        else:
            return response['Items'][0]

    def get_account_by_address(self, address):
        '''
        Gets a account associated to a given account id
        Parameters:
            address = account id
        '''
        response = self.account_table.query(KeyConditionExpression=Key('address').eq(address))

        if len(response['Items']) == 0:
            return None
        else:
            return response['Items'][0]

    def _check_account(self, account):
        if (account is None) or (not account['public_key']) or (not account['email']):
            return False
        else:
            return True
