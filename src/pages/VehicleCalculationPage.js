import React, { useState, useEffect } from 'react';
import { getVehicleCalculations } from '../services/api';

function VehicleCalculationPage() {
  const [calculations, setCalculations] = useState([]);

  useEffect(() => {
    fetchCalculations();
  }, []);

  const fetchCalculations = async () => {
    try {
      const data = await getVehicleCalculations();
      setCalculations(data);
    } catch (error) {
      // Handle error
    }
  };

  return (
    <div className="vehicle-calculation-page">
      <h1>Kalkulasi Kilometer Armada</h1>
      <table>
        <thead>
          <tr>
            <th>ID Armada</th>
            <th>Nama Armada</th>
            <th>Total Kilometer</th>
            <th>Periode</th>
          </tr>
        </thead>
        <tbody>
          {calculations.map((calc) => (
            <tr key={calc.id}>
              <td>{calc.vehicleId}</td>
              <td>{calc.vehicleName}</td>
              <td>{calc.totalKilometers} km</td>
              <td>{calc.period}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default VehicleCalculationPage;