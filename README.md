
# Execution Guide: Macro Recorder Project

This document explains how to set up and run the **Macro Recorder** project. 
This project is a GUI-based macro recorder that captures mouse and keyboard events and transmits them to a WebSocket server in real-time.
---
### Download
- To use the Macro Recorder without setting up a Python environment
[click here main.exe download](https://github.com/gmyun1999/macro_recorder/releases/download/v1.0.0/main.exe)

## 1. Prerequisites

### Required Software:
- Python **3.11** or higher.
- Use `pipenv` for dependency management:
  ```bash
  pip install pipenv
  ```

### Environment Setup:
- The server must be able to handle WebSocket connections.
- Allow connections from `http://localhost` or `http://127.0.0.1`.

---

## 2. Features Overview

### Macro Recorder:
- Captures **mouse** events (clicks, movements) and **keyboard** events (key presses).
- Stores captured data in JSON format with precise timestamps.
- Transmits event data to the WebSocket server in real-time.

### WebSocket Server:
- Maintains a persistent connection with a single client.
- Processes data received from the recorder.
- Requires clients to send regular `ping` messages to maintain the connection.

---

## 3. Project Setup and Execution

### 1. Clone the Project
Clone the project from GitHub and navigate to the project directory:
```bash
git clone https://github.com/gmyun1999/macro_recorder.git
cd macro_recorder
```

### 2. Install Dependencies
Create a virtual environment using `pipenv` and install the required dependencies:
```bash
pipenv install
```

### 3. Activate the Virtual Environment
Activate the `pipenv` virtual environment:
```bash
pipenv shell
```

### 4. Run the Macro Recorder
Run the `main.py` file to start the macro recorder and the server simultaneously. The WebSocket server starts automatically when `main.py` is executed:
```bash
python main.py
```

---

## 4. Download the Executable File
To use the Macro Recorder without setting up a Python environment, you can download the pre-built `.exe` file from the [Releases](https://github.com/gmyun1999/macro_recorder/releases) section on GitHub. Follow these steps:
1. Navigate to the **Releases** section of the repository.
2. Download the latest version of the `macro_recorder.exe` file.
3. Run the `.exe` file directly to start the recorder and server.

---

## 5. Client Sample Code
If you want to connect to the Macro Recorder server as a client, refer to the following example code:

`client_sample_code.py`:
```python
import asyncio
import websockets
import json

async def wait_for_connection():
    uri = "ws://localhost:6281/ws"  # WebSocket server
    timeout = 30  

    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to WebSocket")

            # send ping every 10 seconds(keep-alive) not always 10 seconds
            async def send_ping():
                while True:
                    await asyncio.sleep(10)
                    ping_message = {"type": "ping"}
                    await websocket.send(json.dumps(ping_message))
                    print("Sent: ping")

            async def receive_data():
                while True:
                    try:
                        message = await websocket.recv()
                        print("Received from GUI:", message)
                    except websockets.ConnectionClosed:
                        print("Connection closed")
                        break

            await asyncio.gather(send_ping(), receive_data())

    except asyncio.TimeoutError:
        print("Timeout: Could not connect within 30 seconds.")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(wait_for_connection())
```

### Key Features:
- Connects to the WebSocket server on port `6281`.
- Sends `ping` messages every 10 seconds to maintain the connection.
- Receives and prints messages from the server.

---

## 6. Data Transmission Format
The following JSON data structures are transmitted to the server in real-time:

### Mouse Events:
```json
{
  "type": "mouse_click",
  "timestamp": 1.234,
  "x": 100,
  "y": 200,
  "button": "left",
  "pressed": true
}

{
  "type": "mouse_move",
  "timestamp": 2.345,
  "x": 150,
  "y": 250
}
```

### Keyboard Events:
```json
{
  "type": "keyboard_press",
  "timestamp": 1.567,
  "key": "a"
}
```

---

## 7. Important Notes

### Ping Messages:
- The client must send **regular `ping` messages** to maintain the WebSocket connection. If no `ping` is received, the server assumes the client has disconnected and closes the connection after a timeout.

#### Ping Message Example:
```json
{
  "type": "ping"
}
```

- The server responds with a `pong` message:
```json
{
  "type": "pong",
  "data": null
}
```

### WebSocket-Dependent GUI:
- The GUI operates only when the WebSocket connection is active. Ensure the WebSocket server is running, and the client is successfully connected before interacting with the GUI.

---

## 8. Command Summary

| Step                | Command                                   |
|---------------------|-------------------------------------------|
| Clone the Project   | `git clone https://github.com/gmyun1999/macro_recorder.git` |
| Install Dependencies| `pipenv install`                         |
| Activate Virtual Env| `pipenv shell`                           |
| Run Recorder & Server| `python main.py`                        |

---
