const mqtt = require('mqtt');

// MQTT Configuration
const MQTT_BROKER = 'mqtt://localhost:1883';
const MQTT_TOPIC = 'gps/location';

// Create MQTT client
const client = mqtt.connect(MQTT_BROKER);

// Handle connection
client.on('connect', () => {
    console.log('Connected to MQTT broker');
    console.log(`Subscribing to topic: ${MQTT_TOPIC}`);
    
    client.subscribe(MQTT_TOPIC, (err) => {
        if (err) {
            console.error('Subscription error:', err);
        } else {
            console.log('Subscribed successfully\n');
            console.log('Waiting for messages...\n');
        }
    });
});

// Handle incoming messages
client.on('message', (topic, message) => {
    try {
        const data = JSON.parse(message.toString());
        const timestamp = new Date(data.timestamp * 1000).toLocaleString();
        
        console.log('─'.repeat(50));
        console.log('New Location Update:');
        console.log('─'.repeat(50));
        console.log(`Time: ${timestamp}`);
        console.log(`Latitude: ${data.latitude.toFixed(6)}`);
        console.log(`Longitude: ${data.longitude.toFixed(6)}`);
        console.log('─'.repeat(50), '\n');
    } catch (error) {
        console.error('Error processing message:', error);
    }
});

// Handle errors
client.on('error', (error) => {
    console.error('MQTT Error:', error);
});

// Handle disconnection
client.on('close', () => {
    console.log('Disconnected from MQTT broker');
});

// Handle process termination
process.on('SIGINT', () => {
    console.log('\nClosing MQTT connection...');
    client.end();
    process.exit();
});
