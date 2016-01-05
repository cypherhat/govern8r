import requests
from wallet import NotaryWallet
import configuration

config = configuration.NotaryConfiguration("Client")

wallet = NotaryWallet("foobar")


## Test GET pubkey
req_pubkey = requests.get(config.get_server_url()+'/api/v1/pubkey')
data = req_pubkey.json()
other_party_public_key = data['public_key']
print data['public_key']