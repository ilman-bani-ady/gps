import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, useLocation } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import AddUserPage from './pages/AddUserPage';
import HomePage from './pages/HomePage';
import VehicleListPage from './pages/VehicleListPage';
import VehicleCalculationPage from './pages/VehicleCalculationPage';
import Header from './components/Layout/Header';
import Sidebar from './components/Layout/Sidebar';
import Footer from './components/Layout/Footer';
import './App.css';

function AppContent() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const location = useLocation();
  const isLoginPage = location.pathname === '/login';
  const isHomePage = location.pathname === '/';

  const openNav = () => {
    setIsSidebarOpen(true);
  };

  const closeNav = () => {
    setIsSidebarOpen(false);
  };

  return (
    <div className="app">
      {!isLoginPage && <Header openNav={openNav} />}
      {!isLoginPage && <Sidebar isOpen={isSidebarOpen} closeNav={closeNav} />}
      <div id="main" style={{ 
        marginLeft: isSidebarOpen ? '200px' : '0',
        padding: isHomePage ? '0' : '20px'
      }}>
        <main>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/add-user" element={<AddUserPage />} />
            <Route path="/" element={<HomePage />} />
            <Route path="/vehicles" element={<VehicleListPage />} />
            <Route path="/calculations" element={<VehicleCalculationPage />} />
            {/* <Route path="/add-vehicle" element={<AddVehiclePage />} /> */}
          </Routes>
        </main>
      </div>
      {!isLoginPage && !isHomePage && <Footer />}
    </div>
  );
}

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App;