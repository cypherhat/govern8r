import requests
import json
from wallet import NotaryWallet
from bitcoinlib.wallet import P2PKHBitcoinAddress
from message import SecureMessage

wallet = NotaryWallet("foobar")
secure_message = SecureMessage(wallet)

## Test GET pubkey
req_pubkey = requests.get('https://127.0.0.1:5000/govern8r/api/v1/pubkey',verify=False)
data = req_pubkey.json()
other_party_public_key = data['public_key']
print data['public_key']
address = str(wallet.get_bitcoin_address())

## Test POST account

print("\nWallet Public Key Hex %s" % wallet.get_public_key_hex())
print("\nWallet Public Key %s" % wallet.get_public_key())
addrfromhex = P2PKHBitcoinAddress.from_pubkey(wallet.get_public_key_hex().decode("hex"))
print("\nAddress From Hex %s" % addrfromhex)
email = 'jeff_ploughman@troweprice.com'

registration_message = {'public_key': wallet.get_public_key_hex(), 'email': email}

registration_payload = secure_message.create_secure_payload(other_party_public_key, json.dumps(registration_message))
response = requests.put('https://127.0.0.1:5000/govern8r/api/v1/account/' + address, data=registration_payload,verify=False)
print(response.status_code)
