const mqtt = require('mqtt');
const fs = require('fs');

// MQTT Configuration
const MQTT_BROKER = 'mqtt://localhost:1883';
const MQTT_TOPIC = 'gps/location';

// Create MQTT client
const client = mqtt.connect(MQTT_BROKER);

// Log to console and optional file
const logMessage = (message) => {
    console.log(message);
    // Uncomment below to enable logging to a file
    // fs.appendFileSync('mqtt_logs.txt', message + '\n');
};

// Handle connection
client.on('connect', () => {
    logMessage('Connected to MQTT broker');
    logMessage(`Subscribing to topic: ${MQTT_TOPIC}`);
    
    client.subscribe(MQTT_TOPIC, (err) => {
        if (err) {
            logMessage(`Subscription error: ${err.message}`);
        } else {
            logMessage('Subscribed successfully');
            logMessage('Waiting for messages...\n');
        }
    });
});

// Handle incoming messages
client.on('message', (topic, message) => {
    try {
        const data = JSON.parse(message.toString());
        const timestamp = new Date(data.timestamp * 1000).toLocaleString();
        
        const output = `
${'─'.repeat(50)}
New Location Update:
${'─'.repeat(50)}
Device ID  : ${data.device_id}
Time       : ${timestamp}
Latitude   : ${data.latitude.toFixed(6)}
Longitude  : ${data.longitude.toFixed(6)}
${'─'.repeat(50)}\n`;

        logMessage(output);
    } catch (error) {
        logMessage(`Error processing message: ${error.message}`);
    }
});

// Handle errors
client.on('error', (error) => {
    logMessage(`MQTT Error: ${error.message}`);
});

// Handle disconnection
client.on('close', () => {
    logMessage('Disconnected from MQTT broker');
});

// Handle process termination
process.on('SIGINT', () => {
    logMessage('\nClosing MQTT connection...');
    client.end(() => {
        logMessage('MQTT connection closed');
        process.exit();
    });
});
