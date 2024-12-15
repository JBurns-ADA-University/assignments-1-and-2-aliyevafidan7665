# Import required libraries
import json                         # For reading JSON configuration
import time                        # For sleep operations and timing
import subprocess                  # For managing UBS server process
import requests                    # For making HTTP requests to UBS
from datetime import datetime      # For timestamp creation
import logging                     # For logging functionality
from logging.handlers import RotatingFileHandler  # For log file rotation
import sys                         # For system operations
import signal                      # For handling system signals
import os                          # For operating system operations

class Webmon:
    """
    Webmon class: Monitors and manages the Unreliable Banking Server (UBS).
    Implements monitoring, logging, and server management functionality.
    """
    
    def __init__(self, config_file="webmon.json"):
        """
        Initialize Webmon instance.
        Args:
            config_file (str): Path to configuration file (default: webmon.json)
        """
        # Load configuration from JSON file
        self.config = self._load_config(config_file)
        # Initialize UBS process tracker to None
        self.ubs_process = None
        # Set up logging system
        self.setup_logging()
        
    def _load_config(self, config_file):
        """
        Load and validate the configuration file.
        Args:
            config_file (str): Path to configuration file
        Returns:
            dict: Validated configuration dictionary
        Raises:
            ValueError: If configuration is invalid
            FileNotFoundError: If config file doesn't exist
            JSONDecodeError: If JSON is invalid
        """
        try:
            # Open and read JSON file
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            # Check if main config section exists
            if 'webmonconfig' not in config:
                raise ValueError("Missing 'webmonconfig' in configuration")
            
            webmonconfig = config['webmonconfig']
            # Validate required configuration fields
            required_fields = ['waittime', 'logto']
            for field in required_fields:
                if field not in webmonconfig:
                    raise ValueError(f"Missing required field '{field}' in webmonconfig")
            
            return webmonconfig
            
        except FileNotFoundError:
            # Handle missing configuration file
            print(f"Configuration file {config_file} not found")
            sys.exit(1)
        except json.JSONDecodeError:
            # Handle invalid JSON format
            print(f"Invalid JSON in configuration file {config_file}")
            sys.exit(1)
            
    def setup_logging(self):
        """
        Set up logging system based on configuration.
        Supports file system ('fs') and MongoDB logging.
        """
        if self.config['logto'] == 'fs':
            # Set up rotating file handler (1MB per file, keep 5 backup files)
            handler = RotatingFileHandler('webmon.log', maxBytes=1024*1024, backupCount=5)
            # Set log format with timestamp
            handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
            self.logger = logging.getLogger('webmon')
            self.logger.setLevel(logging.INFO)
            self.logger.addHandler(handler)
        elif self.config['logto'] == 'mongodb':
            # MongoDB logging implementation placeholder
            pass
            
    def start_ubs(self):
        """
        Start the UBS server process.
        Launches server.py in a separate process and logs the event.
        """
        # Check if process doesn't exist or has terminated
        if self.ubs_process is None or self.ubs_process.poll() is not None:
            try:
                # Launch UBS server as a subprocess
                self.ubs_process = subprocess.Popen([sys.executable, 'server.py'])
                self.logger.info("Started UBS server")
                # Wait for server to initialize
                time.sleep(2)
            except Exception as e:
                # Log and exit if server start fails
                self.logger.error(f"Failed to start UBS server: {str(e)}")
                sys.exit(1)

    def stop_ubs(self):
        """
        Stop the UBS server process.
        Attempts graceful termination, forces kill if necessary.
        """
        if self.ubs_process:
            # Try graceful termination
            self.ubs_process.terminate()
            try:
                # Wait up to 5 seconds for process to end
                self.ubs_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # Force kill if graceful termination fails
                self.ubs_process.kill()
            self.logger.info("Stopped UBS server")

    def restart_ubs(self):
        """
        Restart the UBS server.
        Stops the current process and starts a new one.
        """
        self.stop_ubs()
        # Wait for clean shutdown
        time.sleep(1)
        self.start_ubs()
        self.logger.info("Restarted UBS server")

    def check_server_status(self):
        """
        Check UBS server status by making HTTP request.
        Returns:
            int/str: HTTP status code or 'timeout' or None on connection error
        """
        try:
            # Make request with configured timeout
            response = requests.get('http://localhost:8080/getbalance', 
                                 timeout=self.config['waittime']/1000)  # Convert ms to seconds
            return response.status_code
        except requests.Timeout:
            # Handle timeout case
            return 'timeout'
        except requests.RequestException:
            # Handle connection errors
            return None

    def handle_response(self, status):
        """
        Handle server response based on configuration rules.
        Args:
            status: HTTP status code or 'timeout' or None
        """
        if status is None:
            # Handle connection failure
            self.logger.error("Failed to connect to UBS server")
            self.restart_ubs()
            return

        # Handle timeout with immediate restart
        if status == 'timeout':
            self.logger.info("Timeout exceeded waittime - immediate restart required")
            self.restart_ubs()
            return

        # Handle HTTP status codes with retry logic
        status_key = f'http{status}'
        if status_key in self.config:
            rule = self.config[status_key]
            retry_count = 0
            
            # Apply retry logic based on configuration
            while retry_count < rule['retrytimes']:
                time.sleep(1)  # Wait before retry
                new_status = self.check_server_status()
                if new_status != status:
                    break
                retry_count += 1

            # Apply restart action if configured and retries exhausted
            if retry_count == rule['retrytimes'] and rule['action'] == 'restart':
                self.logger.info(f"Restarting server after {retry_count + 1} occurrences of {status_key}")
                self.restart_ubs()

    def run(self):
        """
        Main monitoring loop.
        Starts UBS server and continuously monitors its status.
        """
        # Initial server start
        self.start_ubs()
        
        def signal_handler(signum, frame):
            """Handle system signals for clean shutdown"""
            self.logger.info("Shutting down webmon")
            self.stop_ubs()
            sys.exit(0)
        
        # Register signal handlers for clean shutdown
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        # Main monitoring loop
        while True:
            status = self.check_server_status()
            self.handle_response(status)
            time.sleep(1)  # Prevent CPU overuse

# Entry point to the code
if __name__ == "__main__":
    webmon = Webmon()
    webmon.run()