# tests/test_server.py
import unittest
from server.server import FederatedServer
from server.utils.config_parser import parse_config

class TestServer(unittest.TestCase):
    def setUp(self):
        config = parse_config('configs/server_config.yaml')
        self.server = FederatedServer(config)

    def test_server_initialization(self):
        self.assertIsNotNone(self.server)

    def test_aggregation(self):
        # Test aggregation logic
        pass

if __name__ == '__main__':
    unittest.main()
