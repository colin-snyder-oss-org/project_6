#!/bin/bash

source venv/bin/activate

CLIENT_ID=""
CONFIG_FILE="configs/client_config.yaml"

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --client_id) CLIENT_ID="$2"; shift ;;
        --config) CONFIG_FILE="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

if [ -z "$CLIENT_ID" ]; then
    echo "Client ID not specified. Use --client_id to specify."
    exit 1
fi

python client/client.py --client_id $CLIENT_ID --config $CONFIG_FILE
