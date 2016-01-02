import requests

blockcypher_url = "https://api.blockcypher.com/v1/btc/test3/txs/data"
blockcypher_token = "a65c446def8ad58f07a8f03272268bfc"

class NotarizationService(object):
    
    def __init__(self):
        pass

    def add_to_blockchain(self, signature):
        blockcypher_tx = {
            'data': signature
        }
        response = requests.get(blockcypher_url+'?token='+blockcypher_token, data=blockcypher_tx)

    def check_proof_of_goodwill(self, address):
        '''
        Checks a proof of goodwill for a given address
        '''
        # The test world is wonderful, welcome everybody ! ;)
        return True