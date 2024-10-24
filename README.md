# Unreliable HTTP Server and Client

This project implements an "unreliable" HTTP server that randomly returns different HTTP outcomes for the `/getbalance` route, including timeouts and HTTP errors. It also logs all requests and allows fetching the logs via a `/getlogs` route. A client is provided to interact with the server and test its behavior.


## Features
- **/getbalance**: Randomly returns HTTP 200, 403, 500, or simulates a timeout.
- **/getlogs**: Returns logs of all requests made to the server in JSON format.
- **Client**: Sends multiple requests to the server and fetches logs for analysis.


## Requirements

- Python 3+
- `requests` library (for the client)
- Basic knowledge of command-line and HTTP operations


## Setup Instructions

### 1. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/unreliable-http-server.git
cd unreliable-http-server
```

### Set Up a Virtual Environment

#### For Linux / macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

#### For Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Running the Server
```bash
python server.py
```

### Running the Client
```bash
chmod +x client.sh. # To make the script executable

```
```bash
./client.sh <server_ip> <port>
```

#### This will send multiple requests to the server's /getbalance route and print the results to server.log file. The client will also fetch the server logs from the /getlogs route and display them.

### Testing

#### To modify the number of requests the client sends, you can edit the main function in client.py and change the number of iterations for the requests:
```bash
for i in range(100):  # Change 100 to any desired number of requests
```