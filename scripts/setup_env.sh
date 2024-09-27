#!/bin/bash

python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
protoc -I=./proto --python_out=./common ./proto/federated.proto
