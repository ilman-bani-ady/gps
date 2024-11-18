import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import toast from 'react-hot-toast';
import '../styles/VehicleStyles.css';

function AddVehiclePage() {
  const [vehicle, setVehicle] = useState({
    device_id: '',
    device_name: '',
    phone_number: '',
    reg_no: ''
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setVehicle(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Menyiapkan data sesuai format API
      const deviceData = {
        device_id: vehicle.device_id,
        device_name: vehicle.device_name,
        phone_number: vehicle.phone_number,
        reg_no: vehicle.reg_no
      };

      await axios.post('http://localhost:3013/api/devices', deviceData);
      toast.success('Vehicle added successfully!');
      navigate('/vehicles');
    } catch (err) {
      console.error('Error adding vehicle:', err);
      toast.error(err.message || 'Failed to add vehicle');
    }
  };

  return (
    <div className="add-vehicle-page">
      <h1>Add New Vehicle</h1>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="device_id">Device ID</label>
          <input
            type="text"
            className="form-control"
            id="device_id"
            name="device_id"
            value={vehicle.device_id}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="device_name">Device Name</label>
          <input
            type="text"
            className="form-control"
            id="device_name"
            name="device_name"
            value={vehicle.device_name}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="phone_number">Phone Number</label>
          <input
            type="text"
            className="form-control"
            id="phone_number"
            name="phone_number"
            value={vehicle.phone_number}
            onChange={handleChange}
            required
            pattern="[0-9]{10,13}"
            title="Phone number should be between 10 to 13 digits"
          />
        </div>

        <div className="form-group">
          <label htmlFor="reg_no">Plat NO</label>
          <input
            type="text"
            className="form-control"
            id="reg_no"
            name="reg_no"
            value={vehicle.reg_no}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-actions">
          <button type="submit" className="btn btn-primary me-2">
            Add Vehicle
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

export default AddVehiclePage;