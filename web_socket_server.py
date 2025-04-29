import asyncio
import websockets
import json
import paho.mqtt.publish as publish

MQTT_BROKER = "157.173.101.159"
MQTT_PORT = 1883
MQTT_TOPIC = "relay/wigo_schedule"


async def handle_connection(websocket):
    try:
        async for message in websocket:
            try:
                schedule = json.loads(message)
                print(f"Received schedule: {schedule}")
                on_time = schedule["on"]
                off_time = schedule["off"]

                # Publish MQTT messages
                publish.single(MQTT_TOPIC, payload=f"1 {on_time}", hostname=MQTT_BROKER, port=MQTT_PORT)
                publish.single(MQTT_TOPIC, payload=f"0 {off_time}", hostname=MQTT_BROKER, port=MQTT_PORT)

                await websocket.send(
                    f"Schedule received: ON at {on_time}, OFF at {off_time}"
                )
            except json.JSONDecodeError:
                await websocket.send("Error: Invalid schedule format")
            except KeyError:
                await websocket.send("Error: Missing ON or OFF time")
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")


async def main():
    async with websockets.serve(handle_connection, "localhost", 8765):
        print("WebSocket server started on ws://localhost:8765")
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    asyncio.run(main())
