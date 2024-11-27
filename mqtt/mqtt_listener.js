const mqtt = require('mqtt');

const options = {
    host: 'ip server',
    port: 1883, // Port default MQTT
    clientId: `mqtt_listener_${Math.random().toString(16).slice(2, 8)}`,
};

const client = mqtt.connect(options);

client.on('connect', () => {
    console.log('MQTT listener connected to the server.');

    // Subscribe ke topik tertentu
    client.subscribe('bus/location', (error) => {
        if (error) {
            console.error('Failed to subscribe:', error.message);
        } else {
            console.log('Subscribed to topic: test/topic');
        }
    });
});

client.on('message', (topic, message) => {
    console.log(`Received message on topic "${topic}":`, message.toString());
});

client.on('error', (error) => {
    console.error('Connection error:', error.message);
});

client.on('close', () => {
    console.log('MQTT listener disconnected.');
});
