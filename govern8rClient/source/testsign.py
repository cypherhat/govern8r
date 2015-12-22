from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress
from bitcoin.signmessage import BitcoinMessage, VerifyMessage, SignMessage

key = CBitcoinSecret("L4vB5fomsK8L95wQ7GFzvErYGht49JsCPJyJMHpB4xGM6xgi2jvG")
address = P2PKHBitcoinAddress.from_pubkey(key.pub)  # "1F26pNMrywyZJdr22jErtKcjF8R3Ttt55G"
message = "bitid://localhost:5000/callback?x=8215ed8005bddc3d&u=1"

message = BitcoinMessage(message)

signature = SignMessage(key, message)

print(key, address)
print("Address: %s" % address)
print("Message: %s", message)
print("\nSignature: %s" % signature)
print("\nVerified: %s" % VerifyMessage(address, message, signature))

print("\nTo verify using bitcoin core;")
print("`bitcoin-cli verifymessage %s \"%s\" \"%s\"`" % (address, signature.decode('ascii'), message))
