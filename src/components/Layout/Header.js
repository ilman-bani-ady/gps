import React from 'react';
import { Link } from 'react-router-dom';

function Header({ openNav }) {
  return (
    <header className="app-header">
      <button className="openbtn" onClick={openNav}>
        ☰
      </button>
      <div className="header-content">
        <div className="logo">
          <Link to="/">GPS Fleet Management</Link>
        </div>
      </div>
    </header>
  );
}

export default Header;
