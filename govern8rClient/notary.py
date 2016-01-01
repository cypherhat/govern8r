import argparse

import requests
import json
import hashfile
from wallet import NotaryWallet
from message import SecureMessage
from bitcoinlib.core.key import CPubKey
from bitcoinlib.wallet import P2PKHBitcoinAddress


class Notary(object):
    def __init__(self, notary_url):
        self.notary_url = notary_url
        self.wallet = NotaryWallet()
        self.secure_message = SecureMessage()
        response = requests.get(self.notary_url+'/api/v1/pubkey')
        data = response.json()
        self.other_party_public_key_hex = data['public_key']
        other_party_public_key_decoded = self.other_party_public_key_hex.decode("hex")
        self.other_party_public_key = CPubKey(other_party_public_key_decoded)
        self.other_party_address = P2PKHBitcoinAddress.from_pubkey(self.other_party_public_key)
        self.govenr8r_token = 'UNAUTHENTICATED'

    def register_user(self, email):
        address = str(self.wallet.get_bitcoin_address())
        message = {'public_key': self.wallet.get_public_key_hex(), 'email': email}
        str_message = json.dumps(message)
        payload = self.secure_message.create_secure_payload(self.other_party_public_key_hex, str_message)
        response = requests.put(self.notary_url+'/api/v1/account/' + address, data=payload)
        return response.status_code

    def login(self):
        address = str(self.wallet.get_bitcoin_address())
        response = requests.get(self.notary_url+'/api/v1/challenge/'+address)
        payload = json.loads(response.content)
        if self.secure_message.verify_secure_payload(self.other_party_address, payload):
            message = self.secure_message.get_message_from_secure_payload(payload)
            payload = self.secure_message.create_secure_payload(self.other_party_public_key_hex, message)
            response = requests.put(self.notary_url+'/api/v1/challenge/'+address, data=payload)
            cookies = requests.utils.dict_from_cookiejar(response.cookies)
            self.govenr8r_token = cookies['govenr8r_token']
            return True
        else:
            self.govenr8r_token = 'UNAUTHENTICATED'
            return False

    def logout(self):
        self.govenr8r_token = 'UNAUTHENTICATED'

    @staticmethod
    def confirm_registration(confirmation_url):
        response = requests.get(confirmation_url)
        return response.status_code

    def authenticated(self):
        return self.govenr8r_token != 'UNAUTHENTICATED'

    def notarize_file(self, path_to_file):
        if self.authenticated():
            hash_digest = hashfile.hash_file(path_to_file)
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



