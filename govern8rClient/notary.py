import argparse

import requests
import json
import hashfile
from encrypted_wallet import NotaryWallet
from message import SecureMessage
from bitcoinlib.core.key import CPubKey
from bitcoinlib.wallet import P2PKHBitcoinAddress
from blockcypher import get_transaction_details
from configuration import NotaryConfiguration

config = NotaryConfiguration()

cookies = None


class Notary(object):
    def __init__(self, password):
        self.notary_url = config.get_server_url()
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
        payload = json.loads(response.content)
        print payload
        if config.get_test_mode():
             return payload['confirm_url']
        else:
             return response.status_code

    def login(self):
        global cookies
        address = str(self.wallet.get_bitcoin_address())
        response = requests.get(self.notary_url + '/api/v1/challenge/' + address)
        payload = json.loads(response.content)
        if self.secure_message.verify_secure_payload(self.other_party_address, payload):
            message = self.secure_message.get_message_from_secure_payload(payload)
            payload = self.secure_message.create_secure_payload(self.other_party_public_key_hex, message)
            response = requests.put(self.notary_url + '/api/v1/challenge/' + address, data=payload)
            cookies = requests.utils.dict_from_cookiejar(response.cookies)
            self.govenr8r_token = cookies['govern8r_token']
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
        global cookies
        if not self.authenticated():
            self.login()

        if not self.authenticated():
            print "not able to login"
            return None

        address = str(self.wallet.get_bitcoin_address())

        meta_data = json.loads(metadata_file.read())
        document_hash = hashfile.hash_file_fp(path_to_file)
        meta_data['document_hash'] = document_hash
        print json.dumps(meta_data)
        notarization_payload = self.secure_message.create_secure_payload(self.other_party_public_key_hex,
                                                                         json.dumps(meta_data))


        response = requests.put(self.notary_url + '/api/v1/account/' + address + '/notarization/' + document_hash,
                                cookies=cookies, data=notarization_payload)
        payload = json.loads(response.content)
        print "payload"
        print payload
        if self.secure_message.verify_secure_payload(self.other_party_address, payload):
            message = self.secure_message.get_message_from_secure_payload(payload)
            print message
            message=json.loads(message)
            return message['transaction_hash']

    def notary_status(self, transaction_id):
        status_value = get_transaction_details(transaction_id, coin_symbol="btc-testnet")
        return status_value['confirmed']


def mainMethod(cmd_str=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=['register', 'confirm', 'notarize', 'login', 'notarystatus'],
                        help="Name of the command.")
    parser.add_argument("-password", type=str, help="the password used to access the wallet.")
    parser.add_argument("-email", type=str, help="the email address of the registered user.")
    parser.add_argument("-file", type=file, help="Fully qualified name of the file to notarize.")
    parser.add_argument("-metadata", type=file, help="File containing metadata of the file to notarize.")
    parser.add_argument("-confirm_url", type=str, help="Confirmation URL to confirm an account.")
    parser.add_argument("-transaction_id", type=str, help="Transaction ID of a notary")

    if cmd_str is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(cmd_str)

    notary = Notary(args.password)
    command = args.command

    if not args.password:
        print("Password is required!")
        return

    print "Running " + command + " command"
    if command == "register":
        if not args.email:
            print "register command needs email address"
        else:
            print args.email
            result=notary.register_user(args.email)
            print result
            return result
    elif command == "confirm":
        if not args.confirm_url:
            print "confirm command needs url"
        else:
            print args.confirm_url
            return Notary.confirm_registration(args.confirm_url)
    elif command == "notarize":
        if not args.metadata:
            print "notarize command needs metadata file"
            return

        if not args.file:
            print "notarize command needs file"
            return
        #print args.file
        #print args.metadata
        return notary.notarize_file(args.file, args.metadata)
    elif command == "login":
        return  notary.login()
    elif command == "notarystatus":
        if not args.transaction_id:
            print "confirm command needs transcation_id"
        else:
            print args.transaction_id
            status = notary.notary_status(args.transaction_id)
            print "The Transcation status is"
            print status
            return status
    else:
        print "no command"


if __name__ == "__main__":
    mainMethod()
