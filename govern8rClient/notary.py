import argparse

import requests
import json
from wallet import NotaryWallet
from bitcoinlib.wallet import P2PKHBitcoinAddress
from message import SecureMessage

url='http://127.0.0.1:5000/govern8r'


def main() :
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=['register', 'confirm', 'notary'], help="Name of the command.")
    parser.add_argument("-email", type=str, help="the email address of the registered user.")
    parser.add_argument("-file", type=file, help="Fully qualified name of the file to notarize.")
    parser.add_argument("-confirmurl", type=str, help="Confirmation URL to confirm an account.")
    args = parser.parse_args()
    command = args.command
    print command
    if command == "register":
       print "running register command"
       if( not args.email):
            print "register command needs email address"
       else:
            print args.email
            register_user(args.email)

    elif command == "confirm":
        print "running confirm command"
        if( not args.confirmurl):
            print "confirm command needs url"
        else:
            print args.confirmurl
            confirm_user(args.confirmurl)
    elif command == "notary":

        print "running notary command"
        if( not args.file):
            print "notary command needs file"
        else:
            print args.file
            notarize_file(args.file)
    else:
        print "no command"


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
    address_from_hex = P2PKHBitcoinAddress.from_pubkey(wallet.get_public_key_hex().decode("hex"))
    print("\nAddress From Hex %s" % address_from_hex)

    registration_message = {'public_key': wallet.get_public_key_hex(), 'email': email}

    registration_payload = secure_message.create_secure_payload(other_party_public_key, json.dumps(registration_message))
    response = requests.put(url+'/api/v1/account/' + address, data=registration_payload)
    print(response.status_code)


def confirm_user(confirmation_url):
    print confirmation_url


def notarize_file(path_to_file):
    print path_to_file

if __name__ == "__main__":
    main()



