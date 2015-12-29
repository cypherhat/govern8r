import configparser
import os
from bitcoinlib.wallet import CBitcoinSecret, P2PKHBitcoinAddress
from bitcoin.signmessage import BitcoinMessage, VerifyMessage, SignMessage
import base58

section_name = 'NotaryWallet'
file_name = 'notarywallet.data'


def wallet_exists():
    if os.path.exists(file_name) and os.path.isfile(file_name):
        return True
    else:
        return False


def read_private_key():
    if wallet_exists():
        config = configparser.ConfigParser()
        config.read(file_name)
        if config.has_option(section_name, 'private_key'):
            private_hex = config.get (section_name, 'private_key')
            key = CBitcoinSecret.from_secret_bytes(private_hex)
            return key
        else:
            raise ValueError('Private key does not exist!')
    else:
        raise ValueError('Wallet does not exist!')


def create_new_wallet():
    if wallet_exists():
        raise ValueError('Wallet already exists!')
    # Create private key
    private_key = os.urandom(32)
    private_hex = private_key.encode("hex")

    config = configparser.ConfigParser()
    config.add_section(section_name)
    config.set(section_name, 'private_key',  private_hex)

    with open(file_name, 'w') as configfile:
        config.write(configfile)


class NotaryWallet(object):
    """An encapsulated wallet for notary stuff.

    """
    def __init__(self):
        if not wallet_exists():
            create_new_wallet()
        self.private_key = CBitcoinSecret.from_secret_bytes(read_private_key())
        self.public_key = self.private_key.pub
        self.address = P2PKHBitcoinAddress.from_pubkey(self.public_key)
        print "Notary Wallet created"

    def sign(self, message):
        bitcoin_message = BitcoinMessage(message)
        signature = SignMessage(self.private_key, bitcoin_message)
        return signature

    def verify(self, message, signature):
        bitcoin_message = BitcoinMessage(message)
        return VerifyMessage(self.address, bitcoin_message, signature)

    def get_private_key(self):
        return self.private_key

    def get_public_key(self):
        return self.public_key

    def get_bitcoin_address(self):
        return P2PKHBitcoinAddress.from_pubkey(self.public_key)

    def get_private_key_wif(self):
        return base58.base58_check_encode(0x80, self.private_key)


def main():
    notary_obj = NotaryWallet()
