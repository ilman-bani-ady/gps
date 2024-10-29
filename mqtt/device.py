import paho.mqtt.client as mqtt
broker = "103.245.39.79"
port = 1883
topic = "test/topic"
def on_connect(client, userdata, flags, rc):
    print("Terhubung dengan kode hasil: " + str(rc))
    client.subscribe(topic)
def on_message(client, userdata, msg):
    print(f"Pesan diterima pada topik '{msg.topic}': {msg.payload.decode()}")
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port, 60)
client.loop_start()
input("Tekan Enter untuk keluar...\n")
client.loop_stop()
client.disconnect()