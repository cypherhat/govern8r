import uuid
from datetime import datetime


class Account(object):
    
    def __init__(self, pubkey):
        '''
        Constructor
        Parameters:
            address = bitcoin address associated to the user
        '''
        self.pubkey = pubkey
        # Initializes the uid
        self.uid = str(uuid.uuid4())
        # Sets some additional attributes
        self.created = datetime.now()
        self.signin_count = 0
        
        
        