import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import * as turf from '@turf/turf';
import * as mqtt from 'mqtt/dist/mqtt';
import 'leaflet/dist/leaflet.css';

function Map() {
  const mapRef = useRef(null);
  const mapInstance = useRef(null);
  const markersRef = useRef({});

  useEffect(() => {
    // Coordinates for Jakarta as the center point
    const jakartaCoords = [-6.2088, 106.8456];

    // Initialize the Leaflet map
    const map = L.map(mapRef.current, {
      center: jakartaCoords,
      zoom: 11,
      zoomControl: false,
    });
    mapInstance.current = map;

    // Add a tile layer for the map
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
      subdomains: 'abcd',
      maxZoom: 20,
    }).addTo(map);

    // Create a circle around Jakarta with a radius of 10 km using Turf.js
    const center = turf.point(jakartaCoords);
    const radius = 10;
    const options = { steps: 64, units: 'kilometers' };
    const circle = turf.circle(center, radius, options);

    L.geoJSON(circle, {
      style: {
        color: '#ffffff',
        weight: 2,
        opacity: 0.7,
        fillOpacity: 0.1,
      },
    }).addTo(map);

    L.control.zoom({
      position: 'topright',
    }).addTo(map);

    // Menggunakan WebSocket untuk koneksi MQTT
    const client = mqtt.connect('ws://localhost:1883/mqtt', {
      clientId: `map_client_${Math.random().toString(16).substring(2, 8)}`,
      clean: true,
      connectTimeout: 4000,
      reconnectPeriod: 1000,
    });

    client.on('connect', () => {
      console.log('Connected to MQTT broker');
      client.subscribe('gps/location', (err) => {
        if (!err) {
          console.log('Subscribed to gps/location topic');
        }
      });
    });

    client.on('error', (err) => {
      console.error('MQTT connection error:', err);
    });

    client.on('message', (topic, message) => {
      console.log(`Received message on topic: ${topic}`);
      console.log(`Raw message: ${message.toString()}`);
      
      try {
        const locationData = JSON.parse(message.toString());
        console.log('Parsed message:', locationData);
    
        const { device_id, latitude, longitude } = locationData;
    
        if (!device_id || !latitude || !longitude) {
          console.error('Incomplete data received:', locationData);
          return;
        }
    
        console.log(`Processing data for Device ID: ${device_id}`);
        console.log(`Latitude: ${latitude}, Longitude: ${longitude}`);
    
        const latlng = [parseFloat(latitude), parseFloat(longitude)];
        
        if (markersRef.current[device_id]) {
          console.log(`Updating marker for Device ID: ${device_id}`);
          markersRef.current[device_id].setLatLng(latlng);
          markersRef.current[device_id].getPopup().setContent(`
            <div>
              <strong>Device ID:</strong> ${device_id}<br>
              <strong>Latitude:</strong> ${latitude}<br>
              <strong>Longitude:</strong> ${longitude}<br>
              <strong>Last Update:</strong> ${new Date().toLocaleTimeString()}
            </div>
          `);
        } else {
          console.log(`Creating new marker for Device ID: ${device_id}`);
          const marker = L.marker(latlng)
            .bindPopup(`
              <div>
                <strong>Device ID:</strong> ${device_id}<br>
                <strong>Latitude:</strong> ${latitude}<br>
                <strong>Longitude:</strong> ${longitude}<br>
                <strong>Last Update:</strong> ${new Date().toLocaleTimeString()}
              </div>
            `)
            .addTo(mapInstance.current);
          markersRef.current[device_id] = marker;
        }
      } catch (err) {
        console.error('Error processing MQTT message:', err);
      }
    });

    return () => {
      map.remove();
      client.end();
    };
  }, []);

  return <div ref={mapRef} className="map-container" style={{ height: 'calc(100vh - 60px)' }} />;
}

export default Map;