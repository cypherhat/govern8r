import requests
import json
import hashfile

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
govern8r_token = cookies['govern8r_token']
print("Token from authentication: %s" % govern8r_token)
print("Status: %s" % response.status_code)

#Upload using PUT

file_name = '/Users/tssbi08/govern8r/IP/README.txt'
document_hash = hashfile.hash_file(file_name)
response = requests.get('http://127.0.0.1:5000/govern8r/api/v1/account/' + address + '/document/' + document_hash + '/status', cookies=cookies)
if response.content is not None:
    if response.status_code == 404:
        print ("Document not found!")
    elif response.status_code == 200:
        try:
            files = {'document_content': open(file_name, 'rb')}
            r = requests.put('http://127.0.0.1:5000/govern8r/api/v1/account/'+address+'/document/'+document_hash, cookies=cookies, files=files)
            print r.status_code
        except requests.ConnectionError as e:
           print(e.message)

