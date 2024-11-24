import asyncio
from gmqtt import Client as MQTTClient

# Konfigurasi broker MQTT
BROKER = ' 172.30.102.90'  # Ganti dengan IP broker
PORT = 1883
TOPIC = 'gps/location'
CLIENT_ID = 'pc_receiver'

# Callback saat terhubung
def on_connect(client, flags, rc, properties):
    print(f'Terhubung ke broker MQTT {BROKER}:{PORT}')
    client.subscribe(TOPIC)
    print(f'Subscribed ke topik: {TOPIC}')

# Callback saat menerima pesan
def on_message(client, topic, payload, qos, properties):
    print(f'Terima pesan: {payload.decode()} dari topik: {topic}')

# Fungsi utama
async def main():
    client = MQTTClient(CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message

    # Hubungkan ke broker
    await client.connect(BROKER, PORT)

    # Tetap mendengarkan pesan
    try:
        await asyncio.Future()  # Tunggu tanpa batas waktu
    except asyncio.CancelledError:
        print("Penerimaan dihentikan.")
        await client.disconnect()

# Jalankan loop asyncio
if __name__ == '__main__':
    asyncio.run(main())