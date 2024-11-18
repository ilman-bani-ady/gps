import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import toast from 'react-hot-toast';

function VehicleListPage() {
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDevices();
  }, []);

  const fetchDevices = async () => {
    try {
      const response = await axios.get('http://localhost:3013/api/devices');
      console.log('API Response:', response.data);
      setDevices(response.data.data);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching devices:', err);
      toast.error(err.message || 'Failed to fetch devices');
      setError(err.message);
      setLoading(false);
    }
  };

  const handleDelete = async (deviceId) => {
    if (window.confirm('Are you sure you want to delete this device?')) {
      try {
        await axios.delete(`http://localhost:3013/api/devices/${deviceId}`);
        toast.success('Device deleted successfully!');
        fetchDevices();
      } catch (err) {
        toast.error(err.message || 'Failed to delete device');
        setError(err.message);
      }
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="vehicle-list-page">
      <h1>Vehicle List</h1>
      <Link to="/add-device" className="btn btn-primary mb-3">
        Add New Vehicle
      </Link>
      
      {devices.length === 0 ? (
        <p>No vehicles found</p>
      ) : (
        <table className="table table-striped">
          <thead>
            <tr>
              <th>Device ID</th>
              <th>Device Name</th>
              <th>Phone Number</th>
              <th>Registration Number</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {devices.map((device) => (
              <tr key={device.device_id}>
                <td>{device.device_id}</td>
                <td>{device.device_name}</td>
                <td>{device.phone_number}</td>
                <td>{device.reg_no}</td>
                <td>
                  <Link 
                    to={`/edit-device/${device.device_id}`} 
                    className="btn btn-sm btn-info me-2"
                  >
                    Edit
                  </Link>
                  <button 
                    className="btn btn-sm btn-danger"
                    onClick={() => handleDelete(device.device_id)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default VehicleListPage;