# tests/test_client.py
import unittest
from client.client import FederatedClient
from client.utils.config_parser import parse_config

class TestClient(unittest.TestCase):
    def setUp(self):
        config = parse_config('configs/client_config.yaml')
        self.client = FederatedClient('test_client', config)

    def test_client_initialization(self):
        self.assertIsNotNone(self.client)

    def test_training(self):
        # Test local training logic
        pass

if __name__ == '__main__':
    unittest.main()
