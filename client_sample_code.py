import asyncio
import json

import websockets


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
