# tests/test_secure_aggregation.py
import unittest
from server.secure_aggregation import SecureAggregation
from server.utils.config_parser import parse_config

class TestSecureAggregation(unittest.TestCase):
    def setUp(self):
        config = parse_config('configs/server_config.yaml')
        self.secure_agg = SecureAggregation(config)

    def test_encryption_decryption(self):
        data = {'weights': [1, 2, 3]}
        encrypted_data = self.secure_agg.encrypt(data)
        decrypted_data = self.secure_agg.decrypt(encrypted_data, None)
        self.assertEqual(data, decrypted_data)

if __name__ == '__main__':
    unittest.main()
