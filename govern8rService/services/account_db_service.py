from __future__ import print_function # Python 2/3 compatibility
import boto3
import botocore


class AccountDbService(object):
    
    def __init__(self):
        # Initializes some dictionaries to store accounts
        self._accounts_by_uid = dict()
        self._accounts_by_addr = dict()
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

            print("Account Table status:", account_table.table_status)
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
        if (self.get_account_by_uid(account.uid) is None) and (self.get_account_by_address(account.address) is None):
            # Creates the account in db
            self._accounts_by_uid[account.uid] = account
            self._accounts_by_addr[account.address] = account
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
        if (not self.get_account_by_uid(account.uid) is None) or (not self.get_account_by_address(account.address) is None):
            # Updates the account in db
            self._accounts_by_uid[account.uid] = account
            self._accounts_by_addr[account.address] = account
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
        if (not self.get_account_by_uid(account.uid) is None) or (not self.get_account_by_address(account.address) is None):
            del self._accounts_by_uid[account.uid]
            del self._accounts_by_addr[account.address]
            return True
        else:
            return False        
    
    def get_account_by_uid(self, uid):
        '''
        Gets a account associated to a given account id
        Parameters:
            uid = account id
        '''
        return self._accounts_by_uid.get(uid, None) if uid else None        
    
    def get_account_by_address(self, addr):
        '''
        Gets a account associated to a given bitcoin address
        Parameters:
            addr = bitcoin address
        '''
        return self._accounts_by_addr.get(addr, None) if addr else None                
    
    def _check_account(self, account):
        if (account is None) or (not account.uid) or (not account.address):
            return False
        else:
            return True        
    
        