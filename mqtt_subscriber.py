import paho.mqtt.client as mqtt
import serial
from datetime import datetime
import time

# Serial connection to Arduino
ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=1)
time.sleep(2) 


def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with code {rc}")
    client.subscribe("relay/schedule")


def on_message(client, userdata, msg):
    try:
        message = msg.payload.decode().strip()
        command, scheduled_time = message.split()
        current_time = datetime.now().strftime("%H:%M")
        if current_time == scheduled_time:
            ser.write(b"1" if command == "1" else b"0")
            print(f"Sent {command} to Arduino at {current_time}")
        else:
            print(f"Command {command} ignored, not scheduled for {current_time}")
    except ValueError:
        print(f"Invalid message format: {message}")
    except serial.SerialException:
        print("Serial communication error")
    except Exception as e:
        print(f"Error: {e}")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("157.173.101.159", 1883, 60)
client.loop_forever()
