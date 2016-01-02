import requests
from wallet import NotaryWallet

wallet = NotaryWallet("foobar")


## Test GET pubkey
req_pubkey = requests.get('http://127.0.0.1:5000/govern8r/api/v1/pubkey')
data = req_pubkey.json()
other_party_public_key = data['public_key']
print data['public_key']