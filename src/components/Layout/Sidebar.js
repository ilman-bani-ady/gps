import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { logout } from '../../services/auth'; // Make sure this path is correct

function Sidebar({ isOpen, closeNav }) {
  const navigate = useNavigate();

  const handleSignOut = async () => {
    try {
      await logout(); // Call your logout function
      navigate('/login'); // Redirect to login page after logout
    } catch (error) {
      console.error('Logout failed', error);
      // Handle logout error (show a message to the user, etc.)
    }
  };

  return (
    <div id="mySidebar" className="sidebar" style={{ width: isOpen ? '200px' : '0' }}>
      <a href="javascript:void(0)" className="closebtn" onClick={closeNav}>
        ×
      </a>
      <Link to="/">Home</Link>
      <Link to="/vehicles">Vehicles</Link>
      <Link to="/calculations">Calculations</Link>
      <Link to="/history">History</Link>
      <Link to="/add-user">Add User</Link>
      <a href="#" onClick={handleSignOut} className="sign-out-btn">Sign Out</a>
    </div>
  );
}

export default Sidebar;
