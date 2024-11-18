import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import * as turf from '@turf/turf';
import 'leaflet/dist/leaflet.css';

function Map() {
  const mapRef = useRef(null);

  useEffect(() => {
    // Jakarta coordinates
    const jakartaCoords = [-6.2088, 106.8456];

    // Initialize the map
    const map = L.map(mapRef.current, {
      center: jakartaCoords,
      zoom: 11,
      zoomControl: false
    });

    // Add the dark mode tile layer
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
      subdomains: 'abcd',
      maxZoom: 20
    }).addTo(map);

    // Create a circle around Jakarta using Turf.js
    const center = turf.point(jakartaCoords);
    const radius = 10; // 10 km radius
    const options = { steps: 64, units: 'kilometers' };
    const circle = turf.circle(center, radius, options);

    // Convert Turf circle to Leaflet layer and add to map
    L.geoJSON(circle, {
      style: {
        color: '#ffffff',
        weight: 2,
        opacity: 0.7,
        fillOpacity: 0.1
      }
    }).addTo(map);

    // Add a marker for Jakarta city center
    L.marker(jakartaCoords).addTo(map)
      .bindPopup('Jakarta City Center')
      .openPopup();

    // Add zoom control to a custom position
    L.control.zoom({
      position: 'topright'
    }).addTo(map);

    // Cleanup function
    return () => {
      map.remove();
    };
  }, []);

  return <div ref={mapRef} className="map-container" />;
}

export default Map;