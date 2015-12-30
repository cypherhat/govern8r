import requests
from wallet import NotaryWallet

wallet = NotaryWallet()

req_pubkey = requests.get('http://127.0.0.1:5000/govern8r/api/v1/pubkey')
data = req_pubkey.json()
print data['public_key']

req_account = requests.post('http://127.0.0.1:5000/govern8r/api/v1/account', data={'public_key': wallet.get_public_key_hex(), 'email': 'jeff@foobar.com'})
