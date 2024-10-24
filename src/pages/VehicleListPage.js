import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/VehicleStyles.css';

function VehicleListPage() {
  // Assume you have a list of vehicles stored in state or fetched from an API
  const vehicles = [
    // Your vehicle data here
  ];

  return (
    <div className="vehicle-list-page">
      <h1>Vehicle Management</h1>
      <Link to="/add-vehicle" className="btn btn-primary mb-3">
        Add New Vehicle
      </Link>
      <table className="table table-striped">
        <thead>
          <tr>
            <th>Name</th>
            <th>Model</th>
            <th>Year</th>
            <th>License Plate</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {vehicles.map(vehicle => (
            <tr key={vehicle.id}>
              <td>{vehicle.name}</td>
              <td>{vehicle.model}</td>
              <td>{vehicle.year}</td>
              <td>{vehicle.licensePlate}</td>
              <td>
                <button className="btn btn-sm btn-info mr-2">Edit</button>
                <button className="btn btn-sm btn-danger">Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default VehicleListPage;