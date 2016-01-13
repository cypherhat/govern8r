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
pubkey_response = requests.get('https://127.0.0.1:5000/govern8r/api/v1/pubkey',verify=False)
data = pubkey_response.json()
other_party_public_key_hex = data['public_key']
print data['public_key']
other_party_public_key_decoded = other_party_public_key_hex.decode("hex")
other_party_public_key = CPubKey(other_party_public_key_decoded)
other_party_address = P2PKHBitcoinAddress.from_pubkey(other_party_public_key)
address = str(wallet.get_bitcoin_address())

## Test GET challenge

response = requests.get('https://127.0.0.1:5000/govern8r/api/v1/challenge/'+address,verify=False)
payload = json.loads(response.content)
if secure_message.verify_secure_payload(other_party_address, payload):
    message = secure_message.get_message_from_secure_payload(payload)
    print(message)

payload = secure_message.create_secure_payload(other_party_public_key_hex, message)
response = requests.put('https://127.0.0.1:5000/govern8r/api/v1/challenge/'+address, data=payload,verify=False)
cookies = requests.utils.dict_from_cookiejar(response.cookies)
govern8r_token = cookies['govern8r_token']
print("Token from authentication: %s" % govern8r_token)
print("Status: %s" % response.status_code)

file_name = "/Users/raju/Downloads/jdk-8u65-macosx-x64.dmg"
encrypted_file = "/Users/raju/Downloads/encrypt_jdk-8u65-macosx-x64.dmg"
document_hash = hashfile.hash_file(file_name)

url = 'https://127.0.0.1:5000/govern8r/api/v1/account/' + address + '/document/' + document_hash
local_filename = url.split('/')[-1]
r = requests.get(url, cookies=cookies, allow_redirects=True,verify=False)
with open(local_filename, 'wb') as f:
    for chunk in r.iter_content(chunk_size=1024):
        if chunk:  # filter out keep-alive new chunks
            f.write(chunk)
