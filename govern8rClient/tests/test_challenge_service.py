import requests
import json

from bitcoinlib.core.key import CPubKey
from wallet import NotaryWallet
from bitcoinlib.wallet import P2PKHBitcoinAddress
from message import SecureMessage

wallet = NotaryWallet("foobar")
secure_message = SecureMessage(wallet)

## Test GET pubkey
pubkey_response = requests.get('http://127.0.0.1:5000/govern8r/api/v1/pubkey')
data = pubkey_response.json()
other_party_public_key_hex = data['public_key']
print data['public_key']
other_party_public_key_decoded = other_party_public_key_hex.decode("hex")
other_party_public_key = CPubKey(other_party_public_key_decoded)
other_party_address = P2PKHBitcoinAddress.from_pubkey(other_party_public_key)

address = str(wallet.get_bitcoin_address())

## Test GET challenge

response = requests.get('http://127.0.0.1:5000/govern8r/api/v1/challenge/'+address)
payload = json.loads(response.content)
if secure_message.verify_secure_payload(other_party_address, payload):
    message = secure_message.get_message_from_secure_payload(payload)
    print(message)

payload = secure_message.create_secure_payload(other_party_public_key_hex, message)
response = requests.put('http://127.0.0.1:5000/govern8r/api/v1/challenge/'+address, data=payload)
cookies = requests.utils.dict_from_cookiejar(response.cookies)
print(cookies['govern8r_token'])