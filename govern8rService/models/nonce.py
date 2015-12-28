'''
A model for nonces objects
'''
from datetime import datetime
import hashlib
import os
import random
import time


def to_bytes(x): return x if bytes == str else x.encode()

i2b = chr if bytes == str else lambda x: bytes([x])

b2i = ord if bytes == str else lambda x: x

NONCE_LEN           = 16

class Nonce(object):
    
    # Expiration delay (in seconds)
    EXPIRATION_DELAY = 600
    
    def __init__(self, sid):
        '''
        Constructor
        Parameters:
            sid = session id associated to the nonce
        '''
        self.sid = sid
        self.uid = None
        # Initializes a value for the nonce (let's call that the nonce id)
        self.nid = self.generate_nonce()
        # Sets the creation date
        self.created = datetime.now()
        
    
    def has_expired(self):
        '''
        Checks if nonce has expired
        '''
        delta = datetime.now() - self.created
        return delta.total_seconds() > Nonce.EXPIRATION_DELAY


    def generate_nonce():
        '''
        Generates a random nonce
        Inspired from random_key() in https://github.com/vbuterin/pybitcointools/blob/master/bitcoin/main.py
        Credits to https://github.com/vbuterin
        '''
        entropy = str(os.urandom(32)) + str(random.randrange(2**256)) + str(int(time.time())**7)
        return hashlib.sha256(to_bytes(entropy)).hexdigest()[:NONCE_LEN]

