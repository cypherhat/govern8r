import encrypt
from bitcoinlib.signmessage import BitcoinMessage, VerifyMessage, SignMessage
from bitcoinlib.wallet import CBitcoinSecret, P2PKHBitcoinAddress
import os
import hashlib
from wallet import NotaryWallet



b58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


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


def privateKeyToWif(key_hex):
    return base58CheckEncode(0x80, key_hex.decode('hex'))


wallet = NotaryWallet()

print("\nWallet Private Key %s" % wallet.get_private_key())
print("\nWallet Public Key %s" % wallet.get_public_key())
print("\nWallet Private Key WIF %s" % wallet.get_private_key_wif())
print("\nWallet Address %s" % wallet.get_bitcoin_address())

message = "bitid://localhost:5000/callback?x=30f56bc022dde976&u=1"

print("\nClear: %s" % message)
encrypted = encrypt.encrypt(wallet.get_public_key(), message)
print("\nEncrypted: %s" % encrypted)

decrypted = encrypt.decrypt(wallet.get_private_key_wif(), encrypted)
print("\nDecrypted: %s" % decrypted)

signature = wallet.sign(message)

btcmessage = BitcoinMessage(message)
print("\nSignature: %s" % signature)
print("\nVerified: %s" % VerifyMessage(wallet.get_bitcoin_address(), btcmessage, signature))
print("\nVerified: %s" % wallet.verify(wallet.get_bitcoin_address(), message, signature))
