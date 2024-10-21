import React from 'react';
import { Link } from 'react-router-dom';

function Footer() {
  return (
    <footer className="footer mt-auto py-3 bg-light">
      <div className="container">
        <div className="row">
          <div className="col-md-4">
            <p>GPS Tracking System for Fleet Management</p>
          </div>
          <div className="col-md-4">
            <h5>Quick Links</h5>
            <ul className="list-unstyled">
              <li><Link to="/">Home</Link></li>
              <li><Link to="/vehicles">Vehicles</Link></li>
              <li><Link to="/calculations">Calculations</Link></li>
            </ul>
          </div>
        </div>
        <hr />
        <p className="text-center">&copy; 2024 GPS Fleet Management. All rights reserved.</p>
      </div>
    </footer>
  );
}

export default Footer;
