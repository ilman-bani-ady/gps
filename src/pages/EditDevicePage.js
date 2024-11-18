import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';

function EditDevicePage() {
  const { deviceId } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({
    device_name: '',
    phone_number: '',
    reg_no: ''
  });

  useEffect(() => {
    fetchDevice();
  }, [deviceId]);

  const fetchDevice = async () => {
    try {
      const response = await axios.get(`http://localhost:3013/api/devices/${deviceId}`);
      const deviceData = response.data.data;
      setFormData({
        device_name: deviceData.device_name,
        phone_number: deviceData.phone_number,
        reg_no: deviceData.reg_no
      });
      setLoading(false);
    } catch (err) {
      console.error('Error fetching device:', err);
      setError(err.message);
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.put(`http://localhost:3013/api/devices/${deviceId}`, formData);
      toast.success('Device updated successfully!');
      navigate('/vehicles');
    } catch (err) {
      toast.error(err.message || 'Failed to update device');
      setError(err.message);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="container mt-4">
      <h2>Edit Device</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label className="form-label">Device Name</label>
          <input
            type="text"
            className="form-control"
            name="device_name"
            value={formData.device_name}
            onChange={handleChange}
            required
          />
        </div>
        
        <div className="mb-3">
          <label className="form-label">Phone Number</label>
          <input
            type="text"
            className="form-control"
            name="phone_number"
            value={formData.phone_number}
            onChange={handleChange}
            required
          />
        </div>

        <div className="mb-3">
          <label className="form-label">Registration Number</label>
          <input
            type="text"
            className="form-control"
            name="reg_no"
            value={formData.reg_no}
            onChange={handleChange}
            required
          />
        </div>

        <div className="mb-3">
          <button type="submit" className="btn btn-primary me-2">
            Update Device
          </button>
          <button 
            type="button" 
            className="btn btn-secondary"
            onClick={() => navigate('/vehicles')}
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}

export default EditDevicePage;