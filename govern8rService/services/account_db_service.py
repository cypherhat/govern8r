from __future__ import print_function # Python 2/3 compatibility
import boto3
import botocore
from boto3.dynamodb.conditions import Key, Attr



class AccountDbService(object):
    
    def __init__(self):
        # Initializes some dictionaries to store accounts
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://localhost:8000")
        try:
            self.account_table = self.dynamodb.Table('Account')
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                self.create_account_table()



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
        if (self.get_account_by_public_key(account.public_key) is None) and (self.get_account_by_email(account.email) is None):
            # Creates the account in db
            return True
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
        if (not self.get_account_by_public_key(account.public_key) is None) or (not self.get_account_by_email(account.email) is None):
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
        if (not self.get_account_by_public_key(account.public_key) is None) or (not self.get_account_by_email(account.email) is None):
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

        return None
    
    def get_account_by_email(self, addr):
        '''
        Gets a account associated to a given  email
        Parameters:
            addr =  email
        '''
        return None
    
    def _check_account(self, account):
        if (account is None) or (not account.public_key) or (not account.email):
            return False
        else:
            return True        
    
        