import random
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime
import logging
import socket

# Set up the logger
logging.basicConfig(filename='server.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

# Create a list to store logs in memory for returning them in /getlogs
logs = []

from http.server import BaseHTTPRequestHandler, HTTPServer
import random
import time
import logging
import json
from datetime import datetime

# A list to store logs of events
logs = []

class UnreliableHTTPRequestHandler(BaseHTTPRequestHandler):
    
    # Handles incoming GET requests
    def do_GET(self):
        # Check if the request is for /getbalance
        if self.path == '/getbalance':
            self.handle_getbalance()  # Call the handler for /getbalance
        # Check if the request is for /getlogs
        elif self.path == '/getlogs':
            self.handle_getlogs()  # Call the handler for /getlogs
        else:
            # If the path is unrecognized, return 404 Not Found
            self.send_error(404, "Not Found")

    # Handler for /getbalance route
    def handle_getbalance(self):
        # Simulate random outcomes using a probability distribution
        rand_event = random.choices(
            population=[200, 403, 500, 'timeout'],  # Possible outcomes
            weights=[0.5, 0.2, 0.1, 0.2],  # Probabilities: 50%, 20%, 10%, 20%
            k=1  # Return one result
        )[0]

        # Get the IP address of the client making the request
        client_ip = self.client_address[0]

        # Create a log entry template for this event
        log_entry = {
            'timestamp': datetime.now().isoformat(),  # Record the current time
            'client_ip': client_ip,  # Client's IP address
            'event': ''  # Will be updated based on the outcome
        }

        # Handle different events based on the random selection
        if rand_event == 'timeout':
            # Simulate a timeout by making the server sleep
            time.sleep(3)  # Simulate server hanging (but client may time out first)
            log_entry['event'] = 'timeout'
            logs.append(log_entry)  # Add the event to the logs
            logging.info(f'{client_ip} - Timeout occurred')  # Log the event
        elif rand_event == 403:
            # Respond with 403 Forbidden
            self.send_error(403, "Forbidden")
            log_entry['event'] = '403 Forbidden'
            logs.append(log_entry)
            logging.info(f'{client_ip} - 403 Forbidden')
        elif rand_event == 500:
            # Respond with 500 Internal Server Error
            self.send_error(500, "Internal Server Error")
            log_entry['event'] = '500 Internal Server Error'
            logs.append(log_entry)
            logging.info(f'{client_ip} - 500 Internal Server Error')
        else:
            # Respond with 200 OK and return a fake balance
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # Create an HTML response with a fake account balance
            response_html = """
            <html>
            <head><title>Balance</title></head>
            <body>
            <h1>Your Balance</h1>
            <p>Account Balance: $12345.67</p>
            </body>
            </html>
            """
            self.wfile.write(response_html.encode('utf-8'))  # Send the response to the client
            log_entry['event'] = '200 OK'
            logs.append(log_entry)  # Add the event to the logs
            logging.info(f'{client_ip} - 200 OK')

    # Handler for /getlogs route
    def handle_getlogs(self):
        # Respond with 200 OK and send logs in JSON format
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(logs).encode('utf-8'))  # Send the logs as JSON

# Function to start the HTTP server
def run(server_class=HTTPServer, handler_class=UnreliableHTTPRequestHandler, port=8080):
    server_address = ('', port)  # The server listens on all available interfaces
    httpd = server_class(server_address, handler_class)  # Create an instance of the HTTP server
    print(f"Starting HTTP server on port {port}")  # Print a message indicating the server is running
    httpd.serve_forever()  # Start the server to listen for incoming requests indefinitely

# Entry point of the script
if __name__ == '__main__':
    run()  # Start the server
