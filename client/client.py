# client/client.py
import grpc
import threading
import time
import yaml
import logging
import os
import numpy as np
from torch import nn, optim
import torch

from common import federated_pb2_grpc, federated_pb2
from client.trainer import LocalTrainer
from client.utils.logger import setup_logger
from client.utils.config_parser import parse_config
from client.secure_aggregation import SecureAggregation

class FederatedClient:
    def __init__(self, client_id, config):
        self.client_id = client_id
        self.config = config
        self.logger = setup_logger(f'Client-{client_id}', config['client']['log_level'])
        self.secure_agg = SecureAggregation(config)
        self.trainer = LocalTrainer(config, client_id)
        self.channel = grpc.insecure_channel(f"{config['client']['server_host']}:{config['client']['server_port']}")
        self.stub = federated_pb2_grpc.FederatedLearningStub(self.channel)
        self.current_round = 0
        self.logger.info(f"Client {client_id} initialized.")

    def start(self):
        while True:
            # Request global model
            global_model = self.request_global_model()
            if global_model is None:
                self.logger.warning("No global model received. Retrying...")
                time.sleep(5)
                continue
            # Update local model
            self.trainer.update_model(global_model)
            # Train local model
            self.trainer.train()
            # Send model update
            self.send_model_update()
            time.sleep(5)

    def request_global_model(self):
        client_info = federated_pb2.ClientInfo(client_id=self.client_id)
        try:
            response = self.stub.RequestGlobalModel(client_info)
            decrypted_weights = self.secure_agg.decrypt(response.encrypted_weights)
            self.current_round = response.aggregation_round
            self.logger.debug(f"Received global model for round {self.current_round}")
            return decrypted_weights
        except grpc.RpcError as e:
            self.logger.error(f"RPC error: {e}")
            return None

    def send_model_update(self):
        local_weights = self.trainer.get_model_weights()
        encrypted_weights = self.secure_agg.encrypt(local_weights)
        model_update = federated_pb2.ModelUpdate(
            client_id=self.client_id,
            encrypted_weights=encrypted_weights,
            mask=b''  # Add mask if using masking
        )
        try:
            response = self.stub.SendModelUpdate(model_update)
            self.logger.debug(f"Server response: {response.status} - {response.message}")
        except grpc.RpcError as e:
            self.logger.error(f"RPC error: {e}")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Federated Learning Client')
    parser.add_argument('--client_id', type=str, required=True, help='Unique identifier for the client')
    parser.add_argument('--config', type=str, required=True, help='Path to client config file')
    args = parser.parse_args()

    config = parse_config(args.config)
    client = FederatedClient(args.client_id, config)
    client.start()
