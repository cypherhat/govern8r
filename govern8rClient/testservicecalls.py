import requests
from wallet import NotaryWallet
from bitcoinlib.wallet import P2PKHBitcoinAddress

wallet = NotaryWallet()

req_pubkey = requests.get('http://127.0.0.1:5000/govern8r/api/v1/pubkey')
data = req_pubkey.json()
print data['public_key']
print("\nWallet Public Key Hex %s" % wallet.get_public_key_hex())
print("\nWallet Public Key %s" % wallet.get_public_key())
addrfromhex = P2PKHBitcoinAddress.from_pubkey(wallet.get_public_key_hex().decode("hex"))
print("\nAddress From Hex %s" % addrfromhex)

req_account = requests.post('http://127.0.0.1:5000/govern8r/api/v1/account', data={'public_key': wallet.get_public_key_hex(), 'email': 'jeff@foobar.com'})
