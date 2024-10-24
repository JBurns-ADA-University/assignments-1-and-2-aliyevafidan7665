#!/bin/bash

# Check if two arguments are passed (server IP and port)
if [ "$#" -ne 2 ]; then
    echo "Usage: ./client.sh <server_ip> <port>"
    exit 1
fi

# Assign the arguments to variables
SERVER_IP=$1
PORT=$2

# Run the Python client and pass the arguments
python3 client.py $SERVER_IP $PORT
