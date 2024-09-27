# server/differential_privacy.py
import numpy as np

def apply_differential_privacy(model_weights, config):
    epsilon = config['security']['differential_privacy']['epsilon']
    delta = config['security']['differential_privacy']['delta']
    mechanism = config['security']['differential_privacy']['mechanism']
    sensitivity = np.linalg.norm(model_weights, ord=2)
    if mechanism == 'Gaussian':
        noise = np.random.normal(0, sensitivity * np.sqrt(2 * np.log(1.25 / delta)) / epsilon, size=model_weights.shape)
    else:
        raise NotImplementedError(f"Differential privacy mechanism {mechanism} not implemented.")
    noisy_weights = model_weights + noise
    return noisy_weights
