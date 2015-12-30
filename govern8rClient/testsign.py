import encrypt
from wallet import NotaryWallet

wallet = NotaryWallet()

print("\nWallet Private Key %s" % wallet.get_private_key())
print("\nWallet Public Key %s" % wallet.get_public_key())
print("\nWallet Public Key Hex %s" % wallet.get_public_key_hex())
print("\nWallet Private Key WIF %s" % wallet.get_private_key_wif())
print("\nWallet Address %s" % wallet.get_bitcoin_address())

message = "bitid://localhost:5000/callback?x=30f56bc022dde976&u=1"

print("\nClear: %s" % message)
encrypted = encrypt.encrypt(wallet.get_public_key(), message)
print("\nEncrypted: %s" % encrypted)

decrypted = encrypt.decrypt(wallet.get_private_key_wif(), encrypted)
print("\nDecrypted: %s" % decrypted)

signature = wallet.sign(message)

print("\nSignature: %s" % signature)
print("\nVerified: %s" % wallet.verify(message, signature))
