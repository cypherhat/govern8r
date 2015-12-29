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

private_key = privateKeyToWif(os.urandom(32).encode('hex'))

key = CBitcoinSecret(private_key)
address = P2PKHBitcoinAddress.from_pubkey(key.pub)  # "1F26pNMrywyZJdr22jErtKcjF8R3Ttt55G"
message = "bitid://localhost:5000/callback?x=30f56bc022dde976&u=1"

btcmessage = BitcoinMessage(message)

print("\nClear: %s" % message)
encrypted = encrypt.encrypt(key.pub, message)
print("\nEncrypted: %s" % encrypted)

decrypted = encrypt.decrypt(private_key, encrypted)
print("\nDecrypted: %s" % decrypted)

signature = SignMessage(key, btcmessage)

print(key, address)
print("Address: %s" % address)
print("Message: %s", btcmessage)
print("\nSignature: %s" % signature)
print("\nVerified: %s" % VerifyMessage(address, btcmessage, signature))

print("\nTo verify using bitcoin core;")
print("`bitcoin-cli verifymessage %s \"%s\" \"%s\"`" % (address, signature.decode('ascii'), btcmessage))