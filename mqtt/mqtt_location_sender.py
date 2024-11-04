import asyncio
from gmqtt import Client as MQTTClient
import json
import time
import random

# MQTT Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "gps/location"

# GMQTT client setup
client = MQTTClient("gps-sender")

# Callback handlers
async def on_connect(client, flags, rc, properties):
    print(f'Connected to MQTT Broker: {MQTT_BROKER}')

async def on_message(client, topic, payload, qos, properties):
    print(f'Message received: {payload}')

async def on_disconnect(client, packet, exc=None):
    print('Disconnected')

async def on_subscribe(client, mid, qos, properties):
    print('Subscribed')

# Set callbacks
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.on_subscribe = on_subscribe

async def send_location():
    # Connect to broker
    await client.connect(MQTT_BROKER, MQTT_PORT)

    while True:
        try:
            # Replace this with your actual GPS data collection
            location_data = {
                "latitude": -6.225187 + random.uniform(-0.01, 0.01),
                "longitude": 106.855056 + random.uniform(-0.01, 0.01),
                "timestamp": time.time()
            }
            
            # Convert to JSON and publish
            message = json.dumps(location_data)
            client.publish(MQTT_TOPIC, message)
            print(f"Published: {message}")
            
            # Wait before sending next update
            await asyncio.sleep(5)  # Send update every 5 seconds
            
        except Exception as e:
            print(f"Error sending location: {e}")
            await asyncio.sleep(5)

async def main():
    await send_location()

if __name__ == "__main__":
    asyncio.run(main())