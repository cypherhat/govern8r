import argparse

import requests
import json
import hashfile
from wallet import NotaryWallet
from message import SecureMessage
from bitcoinlib.core.key import CPubKey
from bitcoinlib.wallet import P2PKHBitcoinAddress
from blockcypher import get_transaction_details
import configuration

config = configuration.NotaryConfiguration("Client")


class Notary(object):
    def __init__(self, password):
        self.notary_url = config.get_server_url()
        if not password:
            self.wallet = NotaryWallet(config.get_wallet_password())
        else:
            self.wallet = NotaryWallet(password)
        self.secure_message = SecureMessage(self.wallet)
        response = requests.get(self.notary_url + '/api/v1/pubkey')
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
        response = requests.put(self.notary_url + '/api/v1/account/' + address, data=payload)
        return response.status_code

    def login(self):
        address = str(self.wallet.get_bitcoin_address())
        response = requests.get(self.notary_url + '/api/v1/challenge/' + address)
        payload = json.loads(response.content)
        if self.secure_message.verify_secure_payload(self.other_party_address, payload):
            message = self.secure_message.get_message_from_secure_payload(payload)
            payload = self.secure_message.create_secure_payload(self.other_party_public_key_hex, message)
            response = requests.put(self.notary_url + '/api/v1/challenge/' + address, data=payload)
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

    def notarize_file(self, path_to_file, metadata_file):
        if not self.authenticated():
            self.login()

        if not self.authenticated():
            print "not able to login"
            return None

        address = str(self.wallet.get_bitcoin_address())

        with open(metadata_file, 'rb') as meta_fp:
            self.metadata = meta_fp.read()
        document_hash = hashfile.hash_file(path_to_file)
        notarization_payload = self.secure_message.create_secure_payload(self.other_party_public_key_hex,
                                                                         json.dumps(self.metadata))

        response = requests.put(self.notary_url + '/api/v1/account/' + address + '/notarization/' + document_hash,
                                cookies='{ \'govenr8r_token\' :' + self.govenr8r_token + '}', data=notarization_payload)
        payload = json.loads(response.content)
        if self.secure_message.verify_secure_payload(self.other_party_address, payload):
            message = self.secure_message.get_message_from_secure_payload(payload)
            return message['transaction_hash']

    def notary_status(self, transaction_id):
        status_value = get_transaction_details(transaction_id, coin_symbol="btc-testnet")
        return status_value['confirmed']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=['register', 'confirm', 'notarize', 'login', 'notarystatus'],
                        help="Name of the command.")
    parser.add_argument("-password", type=str, help="the password used to access the wallet.")
    parser.add_argument("-email", type=str, help="the email address of the registered user.")
    parser.add_argument("-file", type=file, help="Fully qualified name of the file to notarize.")
    parser.add_argument("-metadata", type=file, help="File containing metadata of the file to notarize.")
    parser.add_argument("-confirm_url", type=str, help="Confirmation URL to confirm an account.")
    args = parser.parse_args()

    notary = Notary(args.password)
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
    elif command == "notarize":

        print "running notarize command"
        if not args.file:
            print "notarize command needs file"
        else:
            print args.file
            print args.metadata
            notary.notarize_file(args.file, args.metadata)
    elif command == "login":
        notary.login()
    elif command == "notarystatus":
        print "running notarystatus command"
        if not args.transactionid:
            print "confirm command needs transcationid"
        else:
            print args.transactionid
            status = Notary.notary_status(args.transcationid)
            print status
    else:
        print "no command"


if __name__ == "__main__":
    main()
