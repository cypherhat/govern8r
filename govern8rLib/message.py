import encrypt
from wallet import NotaryWallet
from bitcoinlib.wallet import P2PKHBitcoinAddress
from bitcoinlib.signmessage import VerifyMessage, BitcoinMessage
from bitcoinlib.core.key import CPubKey


class SecureMessage(object):

    def __init__(self):
        self.wallet = NotaryWallet()
        
    def create_secure_payload(self, other_party_public_key_hex, message):
        other_party_public_key = CPubKey(other_party_public_key_hex.decode("hex"))
        encrypted = encrypt.encrypt(other_party_public_key, message)
        signature = self.wallet.sign(encrypted)
        payload = {'signature': signature, 'message': encrypted}
        return payload
    
    def verify_secure_payload(self, other_party_address, payload):
        message = BitcoinMessage(payload['message'])
        return VerifyMessage(other_party_address, message, payload['signature'])
        
    def get_message_from_secure_payload(self, payload):
        encrypted = payload['message']
        decrypted = encrypt.decrypt(self.wallet.get_private_key_wif(), encrypted)
        return decrypted

