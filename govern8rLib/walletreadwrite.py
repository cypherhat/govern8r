import configparser
import os
from bitcoinlib.wallet import CBitcoinSecret, P2PKHBitcoinAddress
from bitcoin.signmessage import BitcoinMessage, VerifyMessage, SignMessage
import encrypt
from bitcoinlib.core import b2x, x
import hashlib

b58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def read_wallet(file_name, key_name):
    config = configparser.ConfigParser()
    config.read(file_name)
    config.sections()
    private_hex = config[key_name]['private_key']
    key = CBitcoinSecret.from_secret_bytes(private_hex)



def create_new_wallet(file_name, key_name):
    # Create private key
    private_key = os.urandom(32)
    private_hex = private_key.encode("hex")
    key = CBitcoinSecret.from_secret_bytes(private_key)
    private_base58 = base58CheckEncode(0x80, private_hex.decode('hex'))
    public_hex = key.pub.encode("hex")
    public_base58 = base58CheckEncode(0x80, public_hex.decode('hex'))
    address = P2PKHBitcoinAddress.from_pubkey(key.pub)
    str_address = str(address)

    config = configparser.ConfigParser()
    config[key_name] = {}
    section_name = config[key_name]
    section_name['private_key'] = private_hex
    section_name['public_key'] = public_hex
    section_name['public_addr'] = str_address
    section_name['private_base58'] = base58CheckEncode(0x80, private_hex.decode('hex'))
    with open(file_name, 'w') as configfile:
        config.write(configfile)



def base58encode(n):
    result = ''
    while n > 0:
        result = b58[n % 58] + result
        n /= 58
    return result


def countLeadingChars(s, ch):
    count = 0
    for c in s:
        if c == ch:
            count += 1
        else:
            break
    return count


def base256decode(s):
    result = 0
    for c in s:
        result = result * 256 + ord(c)
    return result


def base58CheckEncode(version, payload):
    s = chr(version) + payload
    checksum = hashlib.sha256(hashlib.sha256(s).digest()).digest()[0:4]
    result = s + checksum
    leadingZeros = countLeadingChars(result, '\0')
    return '1' * leadingZeros + base58encode(base256decode(result))
    
    
class NotaryWallet(object):
    """An encapsulated wallet for notary stuff.

    """
    def __init__(self,file_name,key_name):
        self.file_name=file_name
        self.key_name = key_name
        self.key=self.read_wallet(file_name, key_name)
        self.address = P2PKHBitcoinAddress.from_pubkey(self.key.pub)
        print "Notary Wallet created"

    def read_wallet(self,file_name, key_name):

        config = configparser.ConfigParser()
        config.read(file_name)
        config.sections()

        self.private_hex = config[key_name]['private_key']
        self.public_key  = config[key_name]['public_key']
        self.public_addr  = config[key_name]['public_addr']
        self.private_base58 = config[key_name]['private_base58']
        key = CBitcoinSecret.from_secret_bytes(self.private_hex)
        return key


    def sign(self, message):
        btcmessage = BitcoinMessage(message)
        signature = SignMessage(self.key, btcmessage)
        return signature
    def verify(self, message,signature):
        btcmessage = BitcoinMessage(message)
        return VerifyMessage(self.address, btcmessage, signature)
    def encrypt(self, message):
        encrypted = encrypt.encrypt(self.key.pub, message)
        return encrypted
    def decrypt(self, emessage):
         decrypted = encrypt.decrypt(self.private_base58, encrypted)
def main():
    #    writewallet()
#    create_new_wallet("bootstrap.ini","loginid")
    notary_obj = NotaryWallet("bootstrap.ini", "loginid")
