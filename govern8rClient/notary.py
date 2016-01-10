import argparse

import requests
import json
import hashfile
from encrypted_wallet import NotaryWallet
from message import SecureMessage
from bitcoinlib.core.key import CPubKey
from bitcoinlib.wallet import P2PKHBitcoinAddress
from configuration import NotaryConfiguration

config = NotaryConfiguration()
notary  = None


class Notary(object):
    def __init__(self, password):
        '''
           constructs needed objects
        Parameters
        ----------
        password  : takes the password of the wallet

        Returns
        -------

        '''
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
        self.cookies = None

    def register_user(self, email):
        '''
           first step in registering an user to our system.
        Parameters
        ----------
        email   : the email address of the user.

        Returns
        -------
              the http response status code.
        '''
        #prepare the input.
        address = str(self.wallet.get_bitcoin_address())
        message = {'public_key': self.wallet.get_public_key_hex(), 'email': email}
        str_message = json.dumps(message)
        payload = self.secure_message.create_secure_payload(self.other_party_public_key_hex, str_message)

        # send to server
        response = requests.put(self.notary_url + '/api/v1/account/' + address, data=payload)

        #process the response
        if response.status_code != 200:
                 return None
        print response.content
        payload = response.content
        print payload
        return response.status_code
    def rotate_the_cookie (self,response):
        '''
           utility to rotate the cookie.
        Parameters
        ----------
        response

        Returns
        -------

        '''
        if response.cookies is not None:
            self.cookies = None
            self.govenr8r_token = 'UNAUTHENTICATED'
            return


        self.cookies = requests.utils.dict_from_cookiejar(response.cookies)
        if self.cookies is not None:
            self.govenr8r_token = 'UNAUTHENTICATED'
            return

        if 'govern8r_token' in self.cookies:
            self.govenr8r_token = self.cookies['govern8r_token']
        else :
            self.govenr8r_token = 'UNAUTHENTICATED'



    def login(self):
        '''
           the login procedure. I don't takes any parameters. it assumes the wallet was already
           created and  opened during the Notary object construction.
           The login procedure uses the private key to sign the challenge sent by the server.

        Returns
        -------
             basically true or false.

        '''
        #call the server to get the challenge URL.
        self.govenr8r_token = 'UNAUTHENTICATED'
        address = str(self.wallet.get_bitcoin_address())
        response = requests.get(self.notary_url + '/api/v1/challenge/' + address)

        #process the response
        if response.status_code != 200:
                 return False
        payload = json.loads(response.content)
        if self.secure_message.verify_secure_payload(self.other_party_address, payload):
            message = self.secure_message.get_message_from_secure_payload(payload)
            #create another payload with the signed challenge message.
            payload = self.secure_message.create_secure_payload(self.other_party_public_key_hex, message)

            #call the server with secure payload
            response = requests.put(self.notary_url + '/api/v1/challenge/' + address, data=payload)

            #process the response.
            if response.status_code != 200:
                 return False
            self.rotate_the_cookie(response)
            return True
        else:
            self.govenr8r_token = 'UNAUTHENTICATED'
            return False

    def logout(self):
        '''
         basically it clears the cookie stored locally in memory.
        Returns
        -------

        '''

        self.govenr8r_token = 'UNAUTHENTICATED'
        self.cookies = None

    @staticmethod
    def confirm_registration(confirmation_url):
        '''
           Confirmation of the account is generally done out of band using email,etc.
            This code basically takes the url and call the server url as it is to confirm the account.
        Parameters
        ----------
        confirmation_url

        Returns
        -------

        '''
        response = requests.get(confirmation_url)
        return response.status_code

    def authenticated(self):
        '''
          basically checks for the token and if it is there it assumes the use login is done.
        Returns
        -------
             True or False.
        '''
        return self.govenr8r_token != 'UNAUTHENTICATED'

    def notarize_file(self, path_to_file, metadata_file):
        '''
        the main method to notarize a file.
        Parameters
        ----------
        path_to_file   : the fp to the file. ( Not file name). Need to support file name.
        metadata_file  : the fp to the file. ( Not file name). Need to support file name.

        Returns
        -------
           returns the transaction hash and document hash.

        '''
        address = str(self.wallet.get_bitcoin_address())
        meta_data = json.loads(metadata_file.read())

        # hash the file and generate the document hash
        document_hash = hashfile.hash_file_fp(path_to_file)
        meta_data['document_hash'] = document_hash
        print json.dumps(meta_data)
        #create a secure payload
        notarization_payload = self.secure_message.create_secure_payload(self.other_party_public_key_hex,
                                                                         json.dumps(meta_data))

        # make the rest call.
        response = requests.put(self.notary_url + '/api/v1/account/' + address + '/notarization/' + document_hash,
                                cookies=self.cookies, data=notarization_payload)

        #process the response
        if response.status_code != 200:
                 return None
        #store the rotated cookie.
        self.rotate_the_cookie(response)

        #process the returned payload
        payload = json.loads(response.content)
        print "payload"
        print payload
        if self.secure_message.verify_secure_payload(self.other_party_address, payload):
            message = self.secure_message.get_message_from_secure_payload(payload)
            print message
            message = json.loads(message)
            return message

    def upload_file(self, path_to_file):
        '''
        uploads a file to server
        Parameters
        ----------
        path_to_file : give a file pointer,i.e. file pointer. Need change code support file full path name.

        Returns
        -------
         the http status from the server

        '''
        address = str(self.wallet.get_bitcoin_address())
        files = {'files': path_to_file}
        print repr(path_to_file.name)
        print repr(self.notary_url + '/api/v1/upload/' + address + '/name/' + path_to_file.name)

        #call the server
        response = requests.post(self.notary_url + '/api/v1/upload/' + address + '/name/' + path_to_file.name,
                                 cookies=self.cookies, files=files)

        self.rotate_the_cookie(response)
        #process the response
        if response.status_code != 200:
                 return None
        # cookies = requests.utils.dict_from_cookiejar(response.cookies)
        # self.govenr8r_token = cookies['govern8r_token']
        print response.status_code
        return response.status_code

    def notary_status(self, document_hash):
        '''
        This method returns the notary status
        Parameters
        ----------
        document_hash : the document hash value.

        Returns
        -------
             status value.
        '''

        address = str(self.wallet.get_bitcoin_address())
        response = requests.get(
            self.notary_url + '/api/v1/account/' + address + '/notarization/' + document_hash + '/status',
            cookies=self.cookies)

        self.rotate_the_cookie(response)
        if response.status_code != 200:
            print ('No notarization!')
            return None
        elif response.content is not None:
            payload = json.loads(response.content)
            if self.secure_message.verify_secure_payload(self.other_party_address, payload):
                message = self.secure_message.get_message_from_secure_payload(payload)
                print(message)
                return message




def login_if_needed(notary,command):
    needed = True
    if command == 'register' or command == 'confirm' or command == 'login':
         needed = False
    if needed :
       if not notary.authenticated():
            notary.login()
       if not notary.authenticated():
            print "Not able to login. exiting ..."
            return None
    return 'Done'


def main_method(cmd_str=None):
    '''
       main method of notary.
    Parameters
    ----------
    cmd_str  takes the command line input.

    Returns
    -------

    '''
    global notary
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=['register', 'confirm', 'notarize', 'login', 'notarystatus', 'uploadfile'],
                        help="Name of the command.")
    parser.add_argument("-password", type=str, help="the password used to access the wallet.")
    parser.add_argument("-email", type=str, help="the email address of the registered user.")
    parser.add_argument("-file", type=file, help="Fully qualified name of the file.")
    parser.add_argument("-metadata", type=file, help="File containing metadata of the file to notarize.")
    parser.add_argument("-confirm_url", type=str, help="Confirmation URL to confirm an account.")
    parser.add_argument("-transaction_id", type=str, help="Transaction ID of a notary")

    if cmd_str is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(cmd_str)
    if notary is None :
        notary = Notary(args.password)
    command = args.command


    if not args.password:
        print("Password is required!")
        return

    print "Running " + command + " command"

    if login_if_needed(notary,command) == None :
        return


    if command == "register":
        if not args.email:
            print "register command needs email address"
        else:
            print args.email
            result = notary.register_user(args.email)
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
        # print args.file
        # print args.metadata
        return notary.notarize_file(args.file, args.metadata)
    elif command == "uploadfile":

        if not args.file:
            print "upload command needs file"
            return
        # print args.file
        return notary.upload_file(args.file)
    elif command == "login":
        return notary.login()
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
    main_method()
