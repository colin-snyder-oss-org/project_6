from setuptools import setup, find_packages

setup(
    name='federated_learning_framework',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'protobuf',
        'grpcio',
        'grpcio-tools',
        'PyYAML',
        'torch',
        'torchvision',
        'cryptography',
        'scikit-learn',
    ],
)
