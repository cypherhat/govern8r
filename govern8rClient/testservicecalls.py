import requests
from wallet import NotaryWallet
from bitcoinlib.wallet import P2PKHBitcoinAddress
from message import SecureMessage

wallet = NotaryWallet()


## Test GET pubkey
req_pubkey = requests.get('http://127.0.0.1:5000/govern8r/api/v1/pubkey')
data = req_pubkey.json()
other_party_public_key = data['public_key']
print data['public_key']

## Test POST account
print("\nWallet Public Key Hex %s" % wallet.get_public_key_hex())
print("\nWallet Public Key %s" % wallet.get_public_key())
addrfromhex = P2PKHBitcoinAddress.from_pubkey(wallet.get_public_key_hex().decode("hex"))
print("\nAddress From Hex %s" % addrfromhex)
email = 'jeff@foobar.com'
signature = wallet.sign(email)

req_account = requests.post('http://127.0.0.1:5000/govern8r/api/v1/account', data={'public_key': wallet.get_public_key_hex(), 'signature': signature, 'email': email})

## Test PUT challenge
secure_message = SecureMessage(other_party_public_key)
testmessage = {'name': 'value'}
str_message = str(testmessage)
payload = secure_message.create_secure_payload(str_message)
address = str(wallet.get_bitcoin_address())
resp = requests.put('http://127.0.0.1:5000/govern8r/api/v1/challenge/'+address, data=payload)
