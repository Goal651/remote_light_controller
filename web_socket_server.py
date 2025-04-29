import asyncio
import websockets
import json
import os

async def handle_connection(websocket, path):
    try:
        async for message in websocket:
            try:
                schedule = json.loads(message)
                on_time = schedule['on']
                off_time = schedule['off']
                # Publish ON command
                os.system(f'mosquitto_pub -h 157.173.101.159 -p 1883 -t "relay/wigo_schedule" -m "1 {on_time}"')
                # Publish OFF command
                os.system(f'mosquitto_pub -h 157.173.101.159 -p 1883 -t "relay/wigo_schedule" -m "0 {off_time}"')
                await websocket.send(f"Schedule received: ON at {on_time}, OFF at {off_time}")
            except json.JSONDecodeError:
                await websocket.send("Error: Invalid schedule format")
            except KeyError:
                await websocket.send("Error: Missing ON or OFF time")
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

start_server = websockets.serve(handle_connection, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
print("WebSocket server running on ws://localhost:8765")
asyncio.get_event_loop().run_forever()