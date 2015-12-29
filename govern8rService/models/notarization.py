from datetime import datetime


class Notarization(object):
    
    def __init__(self, metadata):
        '''
        Constructor
        Parameters:
            address = bitcoin address associated to the user
        '''
        self.metadata = metadata
        # Sets some additional attributes
        self.created = datetime.now()

        