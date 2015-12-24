from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress
from bitcoin.signmessage import BitcoinMessage, VerifyMessage, SignMessage
import encrypt


key = CBitcoinSecret("L4vB5fomsK8L95wQ7GFzvErYGht49JsCPJyJMHpB4xGM6xgi2jvG")
address = P2PKHBitcoinAddress.from_pubkey(key.pub)  # "1F26pNMrywyZJdr22jErtKcjF8R3Ttt55G"
message = "bitid://localhost:5000/callback?x=30f56bc022dde976&u=1"

btcmessage = BitcoinMessage(message)

print("\nClear: %s" % message)
encrypted = encrypt.encrypt(key.pub, message)
print("\nEncrypted: %s" % encrypted)

decrypted = encrypt.decrypt("L4vB5fomsK8L95wQ7GFzvErYGht49JsCPJyJMHpB4xGM6xgi2jvG", encrypted)
print("\nDecrypted: %s" % decrypted)

signature = SignMessage(key, btcmessage)

print(key, address)
print("Address: %s" % address)
print("Message: %s", btcmessage)
print("\nSignature: %s" % signature)
print("\nVerified: %s" % VerifyMessage(address, btcmessage, signature))

print("\nTo verify using bitcoin core;")
print("`bitcoin-cli verifymessage %s \"%s\" \"%s\"`" % (address, signature.decode('ascii'), btcmessage))