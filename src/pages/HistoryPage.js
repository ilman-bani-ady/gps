import React, { useState, useEffect } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';
// import LocationMap from '../components/LocationMap';
import '../styles/HistoryStyles.css';

function HistoryPage() {
  const [histories, setHistories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedDevice, setSelectedDevice] = useState('all');
  const [devices, setDevices] = useState([]);
  const [selectedLocation, setSelectedLocation] = useState(null);

  useEffect(() => {
    fetchHistories();
    fetchDevices(); // Ambil daftar devices untuk filter
  }, []);

  const fetchDevices = async () => {
    try {
      const response = await axios.get('http://localhost:3013/api/devices');
      setDevices(response.data.data);
    } catch (err) {
      console.error('Error fetching devices:', err);
      toast.error('Failed to fetch devices');
    }
  };

  const fetchHistories = async () => {
    try {
      const response = await axios.get('http://localhost:3013/api/history');
      setHistories(response.data.data);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching histories:', err);
      setError(err.message);
      toast.error('Failed to fetch history data');
      setLoading(false);
    }
  };

  const handleDeviceFilter = (e) => {
    setSelectedDevice(e.target.value);
  };

  const filteredHistories = selectedDevice === 'all'
    ? histories
    : histories.filter(history => history.device_id === selectedDevice);

  const formatDateTime = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString('en-GB', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  const handleViewLocation = (history) => {
    setSelectedLocation({
      latitude: history.latitude,
      longitude: history.longitude,
      deviceId: history.device_id
    });
  };

  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="history-page">
      <h1>Travel History</h1>
      
      <div className="filters mb-3">
        <select 
          className="form-select"
          value={selectedDevice}
          onChange={handleDeviceFilter}
        >
          <option value="all">All Devices</option>
          {devices.map(device => (
            <option key={device.device_id} value={device.device_id}>
              {device.device_name} ({device.device_id})
            </option>
          ))}
        </select>
      </div>

      {selectedLocation && (
        <div className="map-container mb-4">
          <h3>Location View</h3>
          <button 
            className="btn btn-sm btn-secondary mb-2"
            onClick={() => setSelectedLocation(null)}
          >
            Close Map
          </button>
          {/* <LocationMap 
            latitude={selectedLocation.latitude}
            longitude={selectedLocation.longitude}
            deviceId={selectedLocation.deviceId}
          /> */}
        </div>
      )}

      <div className="table-responsive">
        <table className="table table-striped">
          <thead>
            <tr>
              <th>Device ID</th>
              <th>Latitude</th>
              <th>Longitude</th>
              <th>Speed (km/h)</th>
              <th>Recorded At</th>
              <th>Created At</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredHistories.map((history) => (
              <tr key={history.history_id}>
                <td>{history.device_id}</td>
                <td>{Number(history.latitude).toFixed(6)}</td>
                <td>{Number(history.longitude).toFixed(6)}</td>
                <td>{history.speed}</td>
                <td>{formatDateTime(history.recorded_at)}</td>
                <td>{formatDateTime(history.created_at)}</td>
                <td>
                  <button 
                    className="btn btn-sm btn-info"
                    onClick={() => handleViewLocation(history)}
                  >
                    View on Map
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default HistoryPage;