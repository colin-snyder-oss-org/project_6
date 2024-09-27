# server/secure_aggregation.py
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import pickle

class SecureAggregation:
    def __init__(self, config):
        self.config = config
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.public_key = self.private_key.public_key()

    def encrypt(self, data):
        serialized_data = pickle.dumps(data)
        encrypted_data = self.public_key.encrypt(
            serialized_data,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )
        return encrypted_data

    def decrypt(self, encrypted_data, mask):
        decrypted_data = self.private_key.decrypt(
            encrypted_data,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )
        data = pickle.loads(decrypted_data)
        # Remove mask if necessary
        return data
