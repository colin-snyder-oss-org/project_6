# server/server.py
import grpc
from concurrent import futures
import time
import threading
import yaml
import logging
import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

from common import federated_pb2_grpc
from server.aggregator import Aggregator
from server.utils.logger import setup_logger
from server.utils.config_parser import parse_config
from server.secure_aggregation import SecureAggregation
from server.differential_privacy import apply_differential_privacy

class FederatedServer(federated_pb2_grpc.FederatedLearningServicer):
    def __init__(self, config):
        self.config = config
        self.logger = setup_logger('Server', config['server']['log_level'])
        self.aggregator = Aggregator(config)
        self.secure_agg = SecureAggregation(config)
        self.global_model_lock = threading.Lock()
        self.current_round = 0
        self.logger.info("Server initialized.")

    def SendModelUpdate(self, request, context):
        client_id = request.client_id
        encrypted_weights = request.encrypted_weights
        mask = request.mask
        self.logger.debug(f"Received model update from {client_id}")
        
        # Decrypt weights
        decrypted_weights = self.secure_agg.decrypt(encrypted_weights, mask)
        
        # Update aggregator
        with self.global_model_lock:
            self.aggregator.collect_update(client_id, decrypted_weights)
        
        return federated_pb2.ServerResponse(status='OK', message='Model update received')

    def RequestGlobalModel(self, request, context):
        client_id = request.client_id
        self.logger.debug(f"{client_id} requested global model")
        
        with self.global_model_lock:
            global_weights = self.aggregator.get_global_model()
            # Apply differential privacy if enabled
            if self.config['security']['differential_privacy']['enable']:
                global_weights = apply_differential_privacy(global_weights, self.config)
            encrypted_weights = self.secure_agg.encrypt(global_weights)
        
        return federated_pb2.GlobalModel(encrypted_weights=encrypted_weights, aggregation_round=self.current_round)

    def start(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        federated_pb2_grpc.add_FederatedLearningServicer_to_server(self, server)
        server.add_insecure_port(f"{self.config['server']['host']}:{self.config['server']['port']}")
        server.start()
        self.logger.info(f"Server started on {self.config['server']['host']}:{self.config['server']['port']}")
        try:
            while True:
                time.sleep(86400)
        except KeyboardInterrupt:
            server.stop(0)
            self.logger.info("Server stopped.")

if __name__ == '__main__':
    import argparse
    from common import federated_pb2

    parser = argparse.ArgumentParser(description='Federated Learning Server')
    parser.add_argument('--config', type=str, required=True, help='Path to server config file')
    args = parser.parse_args()

    config = parse_config(args.config)
    server = FederatedServer(config)
    server.start()
