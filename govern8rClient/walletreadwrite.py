import configparser
import os
from bitcoinlib.wallet import CBitcoinSecret, P2PKHBitcoinAddress
import encrypt
from bitcoinlib.core import b2x, x

import hashlib

b58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def test_writewallet():
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'ServerAliveInterval': '45',
                         'Compression': 'yes',
                         'CompressionLevel': '9'}
    config['bitbucket.org'] = {}
    config['bitbucket.org']['User'] = 'hg'
    config['topsecret.server.com'] = {}
    topsecret = config['topsecret.server.com']
    topsecret['Port'] = '50022'  # mutates the parser
    topsecret['ForwardX11'] = 'no'  # same here
    config['DEFAULT']['ForwardX11'] = 'yes'
    with open('example1.ini', 'w') as configfile:
        config.write(configfile)


def test_readwallet():
    config = configparser.ConfigParser()
    config.sections()
    config.read('example.ini')
    config.sections()
    print 'bitbucket.org' in config
    print 'bytebong.com' in config
    print config['bitbucket.org']['User']
    print config['DEFAULT']['Compression']
    topsecret = config['topsecret.server.com']
    print topsecret['ForwardX11']
    print topsecret['Port']
    for key in config['bitbucket.org']: print(key)
    print config['bitbucket.org']['ForwardX11']


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


def test_create_new_wallet():
    # Create private key
    private_key = os.urandom(32)
    private_hex = private_key.encode("hex")
    key = CBitcoinSecret.from_secret_bytes(private_key)
    print "private key="
    print key
    private_base58 = base58CheckEncode(0x80, private_hex.decode('hex'))

    print "base58 private key = " + private_base58
    public_hex = key.pub.encode("hex")
    print "public base58" + base58CheckEncode(0x80, public_hex.decode('hex'))
    address = P2PKHBitcoinAddress.from_pubkey(key.pub)
    print "address "
    print str(address)
    testAddr(x(public_hex), str(address))
    testPrivateKey(x(private_hex), str(public_hex), str(address))


def testAddr(pubkey, expected_str_addr):
    addr = P2PKHBitcoinAddress.from_pubkey(pubkey)
    if (str(addr) == expected_str_addr):
        print "True they are equal"
    else:
        print "False they are not equal"


def testPrivateKey(private_key, expected_pub_key, expected_str_addr):
    key = CBitcoinSecret.from_secret_bytes(private_key)
    if (str(key.pub.encode("hex")) == expected_pub_key):
        print "True they are equal"
    else:
        print "False they are not equal"
    address = P2PKHBitcoinAddress.from_pubkey(key.pub)
    if (str(address) == expected_str_addr):
        print "True they are equal"
    else:
        print "False they are not equal"


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


def main():
    #    writewallet()
    #    create_new_wallet("bootstrap.ini","loginid")
    read_wallet("bootstrap.ini", "loginid")


if __name__ == "__main__":
    main()
