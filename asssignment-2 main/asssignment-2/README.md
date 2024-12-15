# Webmon - UBS Server Monitor

## Overview
Webmon is a monitoring system designed to watch and manage the Unreliable Banking Server (UBS). It provides automatic monitoring, restart capabilities, and comprehensive logging of server events.

## Project Structure
```
assignment-2/
├── webmon.py        # Main monitoring component
├── server.py        # UBS server
├── webmon.json      # Configuration file
├── requirements.txt # Project dependencies
├── README.md        # This file
├── webmon.log      # Monitor event logs
└── server.log      # UBS server logs
```

## Requirements
- Python 3.8 or higher
- Required Python packages:
  ```
  requests==2.31.0
  ```

## Installation

1. Clone project directory:
```bash
cd assignment-2
```

2. **Create and Activate Virtual Environment**
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
```bash
pip install -r requirements.txt
```


## Usage

1. Start the monitor:
```bash
python webmon.py
```

2. The monitor will:
- Start the UBS server automatically
- Monitor server responses
- Apply configured rules
- Log all events
- Restart server when needed

3. Monitor server status:
- Check webmon.log for monitor events
- Check server.log for UBS responses

4. Stop the system:
- Press Ctrl+C for clean shutdown
- Both webmon and UBS will stop properly

## Log Files

### webmon.log
Contains monitor events:
```
2024-12-10 15:46:20,399 - Started UBS server
2024-12-10 15:46:24,459 - Restarting server after 2 occurrences of http403
```

### server.log
Contains UBS server responses:
```
2024-12-10 15:46:22,442 - 127.0.0.1 - 200 OK
2024-12-10 15:46:23,450 - 127.0.0.1 - 403 Forbidden
```

## Features
- Automatic UBS server management
- Configurable response handling
- Timeout detection and handling
- Automatic server restarts
- Comprehensive logging
- Clean shutdown handling
- File system logging

## Error Handling
- Invalid configuration detection
- Server start/stop error handling
- Connection error management
- Timeout handling
- Process management

## Testing
To test the system:
1. Start webmon
2. Access http://localhost:8080/getbalance
3. Monitor logs for events
4. Verify restart behavior for:
   - Timeouts
   - Consecutive 403 errors
   - Multiple 500 errors

## Troubleshooting

### Common Issues

1. Server won't start:
- Check if port 8080 is available
- Verify Python path in system
- Check server.py permissions



### Solutions

1. Port in use:
```bash
# Check port usage
netstat -ano | findstr :8080
# Kill process if needed
taskkill /PID [process_id] /F
```


