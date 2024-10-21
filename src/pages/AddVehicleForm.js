import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/VehicleStyles.css';

function AddVehiclePage() {
  const [vehicle, setVehicle] = useState({
    name: '',
    type: '',
    plateNumber: '',
    status: 'active'
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setVehicle(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Here you would typically send the data to your backend API
    console.log('New vehicle:', vehicle);
    // After adding, navigate back to the vehicle list
    navigate('/vehicles');
  };

  return (
    <div className="add-vehicle-page">
      <h1>Add New Vehicle</h1>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Vehicle Name</label>
          <input
            type="text"
            className="form-control"
            id="name"
            name="name"
            value={vehicle.name}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="type">Vehicle Type</label>
          <select
            className="form-control"
            id="type"
            name="type"
            value={vehicle.type}
            onChange={handleChange}
            required
          >
            <option value="">Select a type</option>
            <option value="car">Car</option>
            <option value="truck">Truck</option>
            <option value="van">Van</option>
            <option value="motorcycle">Motorcycle</option>
          </select>
        </div>
        <div className="form-group">
          <label htmlFor="plateNumber">Plate Number</label>
          <input
            type="text"
            className="form-control"
            id="plateNumber"
            name="plateNumber"
            value={vehicle.plateNumber}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="status">Status</label>
          <select
            className="form-control"
            id="status"
            name="status"
            value={vehicle.status}
            onChange={handleChange}
          >
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
            <option value="maintenance">Maintenance</option>
          </select>
        </div>
        <button type="submit" className="btn btn-primary">Add Vehicle</button>
      </form>
    </div>
  );
}

export default AddVehiclePage;
