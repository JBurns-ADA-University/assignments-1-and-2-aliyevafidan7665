import requests
import sys
import time

import requests
import time
import sys

# Main function that communicates with the unreliable HTTP server
def main(server_ip, port):
    # Construct the base URL using the server IP and port
    base_url = f"http://{server_ip}:{port}"
    
    # Endpoint for checking the balance
    getbalance_url = f"{base_url}/getbalance"
    
    # Endpoint for fetching server logs
    getlogs_url = f"{base_url}/getlogs"

    # Call /getbalance multiple times to test the response behavior of the unreliable server
    for i in range(100):  # Loop 100 times to test how the server responds over time
        try:
            print(f"Request {i+1}:")  # Print the current request number
            # Send a GET request to /getbalance
            response = requests.get(getbalance_url, timeout=5)  # Timeout set to 5 seconds

            # If the response status code is 200, assume balance was retrieved successfully
            if response.status_code == 200:
                print("Balance Retrieved Successfully")
            else:
                # Print the status code for any other response (e.g., 500, 404, etc.)
                print(f"Error: Received status code {response.status_code}")
        
        # Handle timeout exceptions
        except requests.exceptions.Timeout:
            print("Error: Request timed out")

        # Catch any other request-related exceptions and print the error
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

        # Pause for 1 second between requests to avoid overwhelming the server
        time.sleep(1)

    # After making several requests, fetch the server logs
    print("\nFetching Logs...")
    try:
        # Send a GET request to /getlogs to retrieve logs from the server
        response = requests.get(getlogs_url, timeout=5)  # Timeout set to 5 seconds

        # If the response status code is 200, parse the logs
        if response.status_code == 200:
            logs = response.json()  # Convert the response to JSON (assuming logs are in JSON format)
            print("Server Logs:")
            # Loop through the logs and print each one
            for log in logs:
                print(log)
        else:
            # Print an error message for non-200 status codes
            print(f"Error: Received status code {response.status_code}")

    # Handle timeout exceptions for the logs request
    except requests.exceptions.Timeout:
        print("Error: Request timed out")

    # Catch any other exceptions and print the error message
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

# Entry point of the script when executed
if __name__ == '__main__':
    # Ensure the correct number of command-line arguments are provided
    if len(sys.argv) != 3:
        print("Usage: ./client.sh <server_ip> <port>")  # Print usage instructions
        sys.exit(1)  # Exit with an error code

    # Extract server IP and port from command-line arguments
    server_ip = sys.argv[1]
    port = int(sys.argv[2])  # Convert port to an integer

    # Call the main function with the server IP and port
    main(server_ip, port)
