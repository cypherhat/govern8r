import argparse

import requests
import json
from wallet import NotaryWallet
from bitcoinlib.wallet import P2PKHBitcoinAddress
from message import SecureMessage


def main() :
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=['register', 'confirm', 'notary'], help="name of the command")
    parser.add_argument("-email", type=str, help="the email address of the registered user")
    parser.add_argument("-file", type=file, help="Fully qualified name of the file to notarize")
    args = parser.parse_args()
    command = args.command
    print command
    if command == "register":
       print "register command"
       if( not args.email):
            print "register command needs email address"
       else:
            print args.email
            register_user(args.email)

    elif command == "confirm":
        print "confirm command"
    elif command == "notary":
        print "notary command"
    else:
        print "no command"


url='http://127.0.0.1:5000/govern8r'

def register_user(email):

    wallet = NotaryWallet()
    ## Test GET pubkey
    req_pubkey = requests.get(url+'/api/v1/pubkey')
    data = req_pubkey.json()
    other_party_public_key = data['public_key']
    print data['public_key']
    secure_message = SecureMessage()
    address = str(wallet.get_bitcoin_address())

    ## Test POST account

    print("\nWallet Public Key Hex %s" % wallet.get_public_key_hex())
    print("\nWallet Public Key %s" % wallet.get_public_key())
    addrfromhex = P2PKHBitcoinAddress.from_pubkey(wallet.get_public_key_hex().decode("hex"))
    print("\nAddress From Hex %s" % addrfromhex)


    registration_message = {'public_key': wallet.get_public_key_hex(), 'email': email}

    registration_payload = secure_message.create_secure_payload(other_party_public_key, json.dumps(registration_message))
    response = requests.put(url+'/api/v1/account/' + address, data=registration_payload)
    print(response.status_code)

if __name__ == "__main__":
     main()



