import argparse

import requests
import json
from wallet import NotaryWallet
from message import SecureMessage


class Notary(object):
    def __init__(self, notary_url):
        self.notary_url = notary_url
        self.wallet = NotaryWallet()
        response = requests.get(self.notary_url+'/api/v1/pubkey')
        data = response.json()
        self.other_party_public_key = data['public_key']

    def register_user(self, email):
        secure_message = SecureMessage()
        address = str(self.wallet.get_bitcoin_address())
        message = {'public_key': self.wallet.get_public_key_hex(), 'email': email}
        str_message = json.dumps(message)
        payload = secure_message.create_secure_payload(self.other_party_public_key, str_message)
        response = requests.put(self.notary_url+'/api/v1/account/' + address, data=payload)
        print(response.status_code)

    @staticmethod
    def confirm_registration(confirmation_url):
        response = requests.get(confirmation_url)
        return response.status_code

    def notarize_file(self, path_to_file):
        print path_to_file


def main():
    notary_url = 'http://127.0.0.1:5000/govern8r'
    notary = Notary(notary_url)
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=['register', 'confirm', 'notary'], help="Name of the command.")
    parser.add_argument("-email", type=str, help="the email address of the registered user.")
    parser.add_argument("-file", type=file, help="Fully qualified name of the file to notarize.")
    parser.add_argument("-confirm_url", type=str, help="Confirmation URL to confirm an account.")
    args = parser.parse_args()
    command = args.command
    print command
    if command == "register":
        print "running register command"
        if not args.email:
            print "register command needs email address"
        else:
            print args.email
            notary.register_user(args.email)

    elif command == "confirm":
        print "running confirm command"
        if not args.confirm_url:
            print "confirm command needs url"
        else:
            print args.confirmurl
            Notary.confirm_registration(args.confirm_url)
    elif command == "notary":

        print "running notary command"
        if not args.file:
            print "notary command needs file"
        else:
            print args.file
            notary.notarize_file(args.file)
    else:
        print "no command"


if __name__ == "__main__":
    main()



