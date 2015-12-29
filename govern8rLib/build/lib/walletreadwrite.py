import configparser
import os
from bitcoinlib.wallet import CBitcoinSecret, P2PKHBitcoinAddress
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
