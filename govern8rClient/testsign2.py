import encrypt
import requests
from bitcoin import *

key  = sha256('L4vB5fomsK8L95wQ7GFzvErYGht49JsCPJyJMHpB4xGM6xgi2jvG')
pubkey = privtopub(key)
address = pubkey_to_address(pubkey)
message = "bitid://localhost:5000/callback?x=30f56bc022dde976&u=1"
print("\nPublic key: %s" % pubkey)

print("\nClear: %s" % message)
encrypted = encrypt.encrypt(pubkey, message)
print("\nEncrypted: %s" % encrypted)
#
decrypted = encrypt.decrypt("L4vB5fomsK8L95wQ7GFzvErYGht49JsCPJyJMHpB4xGM6xgi2jvG", encrypted)
print("\nDecrypted: %s" % decrypted)

signature = ecdsa_sign(message, key)

print(key, address)
print("Address: %s" % address)

print("\nSignature: %s" % signature)
print("\nVerified: %s" % ecdsa_verify(message, signature, pubkey))

