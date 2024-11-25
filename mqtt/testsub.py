import asyncio
from gmqtt import Client as MQTTClient
import time

# Callback when client receives a CONNACK response from the server
def on_connect(client, flags, rc, properties):
    print('Connected')
    client.subscribe('gps/location', qos=1)

# Callback when a message is received from the server
def on_message(client, topic, payload, qos, properties):
    print(f'Topic: {topic}')
    print(f'Payload: {payload.decode()}')
    print('---')

# Callback when client disconnects from the server
def on_disconnect(client, packet, exc=None):
    print('Disconnected')

async def main():
    # Create a unique client ID
    client = MQTTClient('gps_subscriber')
    
    # Set up callbacks
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    
    # Connect to the MQTT broker (using default localhost:1883)
    await client.connect('localhost')
    
    try:
        while True:
            await asyncio.sleep(3)  # Wait for 3 seconds between iterations
    except Exception as e:
        print(f'Error: {e}')
    finally:
        await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())