const mqtt = require('mqtt');

// MQTT Configuration
const MQTT_BROKER = 'mqtt://localhost'; // Adjust if needed
const MQTT_PORT = 1883; // Default MQTT port
const MQTT_TOPIC = 'gps/location';

// Create MQTT client
const client = mqtt.connect(MQTT_BROKER, { port: MQTT_PORT });

// Callback handlers
client.on('connect', () => {
    console.log(`Connected to MQTT Broker: ${MQTT_BROKER}`);
    
    // Subscribe to the GPS location topic
    client.subscribe(MQTT_TOPIC, (err) => {
        if (!err) {
            console.log(`Subscribed to topic: ${MQTT_TOPIC}`);
        } else {
            console.error(`Failed to subscribe: ${err}`);
        }
    });
});

client.on('message', (topic, message) => {
    // Message is a Buffer, convert to string and parse JSON
    const locationData = JSON.parse(message.toString());
    console.log(`Message received: ${JSON.stringify(locationData)}`);
});

// Function to send location data
const sendLocation = () => {
    const latitude = -6.231570 + (Math.random() * 0.02 - 0.01);
    const longitude = 106.867176 + (Math.random() * 0.02 - 0.01);
    const timestamp = Math.floor(Date.now() / 1000);
    
    const locationData = {
        latitude: latitude,
        longitude: longitude,
        timestamp: timestamp,
    };
    
    const message = JSON.stringify(locationData);
    client.publish(MQTT_TOPIC, message, (err) => {
        if (!err) {
            console.log(`Published: ${message}`);
        } else {
            console.error(`Error publishing: ${err}`);
        }
    });
};

// Send location updates every 2 seconds
setInterval(sendLocation, 2000);

// Handle disconnect
client.on('disconnect', () => {
    console.log('Disconnected from MQTT Broker');
});
