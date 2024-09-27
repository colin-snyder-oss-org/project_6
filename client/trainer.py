# client/trainer.py
import torch
from torch import nn, optim
from client.data_loader import get_data_loader
from client.model import NeuralNetwork
from client.utils.logger import setup_logger

class LocalTrainer:
    def __init__(self, config, client_id):
        self.config = config
        self.client_id = client_id
        self.logger = setup_logger(f'Trainer-{client_id}', config['client']['log_level'])
        self.model = NeuralNetwork()
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.SGD(self.model.parameters(), lr=config['client']['learning_rate'])
        self.data_loader = get_data_loader(config['client']['data_path'].format(client_id=client_id), config['client']['batch_size'])
        self.logger.info("Local trainer initialized.")

    def update_model(self, global_weights):
        self.model.load_state_dict(global_weights)
        self.logger.debug("Model updated with global weights.")

    def train(self):
        self.model.train()
        for epoch in range(self.config['client']['epochs']):
            for batch_idx, (data, target) in enumerate(self.data_loader):
                self.optimizer.zero_grad()
                output = self.model(data)
                loss = self.criterion(output, target)
                loss.backward()
                self.optimizer.step()
                if batch_idx % 10 == 0:
                    self.logger.debug(f'Epoch {epoch} Batch {batch_idx} Loss {loss.item()}')

    def get_model_weights(self):
        return self.model.state_dict()
