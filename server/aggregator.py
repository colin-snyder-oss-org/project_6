# server/aggregator.py
import threading
import numpy as np
from server.utils.logger import setup_logger

class Aggregator:
    def __init__(self, config):
        self.config = config
        self.logger = setup_logger('Aggregator', config['server']['log_level'])
        self.updates = []
        self.update_lock = threading.Lock()
        self.global_model = None
        self.current_round = 0
        self.logger.info("Aggregator initialized.")

    def collect_update(self, client_id, weights):
        with self.update_lock:
            self.updates.append(weights)
            self.logger.debug(f"Collected update from {client_id}. Total updates: {len(self.updates)}")
            if len(self.updates) >= self.config['server']['max_clients']:
                self.aggregate_updates()

    def aggregate_updates(self):
        self.logger.info("Aggregating client updates.")
        aggregated_weights = np.mean(np.array(self.updates), axis=0)
        self.global_model = aggregated_weights
        self.updates = []
        self.current_round += 1
        self.logger.info(f"Aggregation round {self.current_round} completed.")

    def get_global_model(self):
        if self.global_model is None:
            raise ValueError("Global model not yet initialized.")
        return self.global_model
