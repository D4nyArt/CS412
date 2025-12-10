// File: App.js
// Author: Daniel Arteaga (d4nyart@bu.edu), 12/9/2025
// Description: Main React component that sets up routing, authentication state, and global layout.

import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Library from './pages/Library';
import './App.css';
import Planner from './pages/Planner';
import ActiveSession from './pages/ActiveSession';
import Stats from './pages/Stats';
import Login from './pages/Login';
import Register from './pages/Register';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  // If Production (Server) -> Use '/d4nyart/project'
  // If Development (Local) -> Use '' (empty string)
  const basename = process.env.NODE_ENV === 'production'
    ? "/d4nyart/project"
    : "";


  // Authentication state
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Use Effect to check for authentication token on component mount
  useEffect(() => {
    // Check token on mount to persist login state on refresh
    const token = localStorage.getItem('token');
    setIsAuthenticated(!!token);
  }, []);

  // Handler for user logout
  const handleLogout = () => {
    // Clear local storage to remove token
    localStorage.clear();
    setIsAuthenticated(false);
    // Redirect to login page
    window.location.href = basename + '/login';
    // Hard redirect is safe for logout to clear memory.
  };

  return (
    <Router basename={basename}>
      <div className="app-container">
        <div className="content-wrap">
          <Routes>
            {/* Public Routes */}
            <Route path="/register" element={<Register setIsAuthenticated={setIsAuthenticated} />} />
            <Route path="/login" element={<Login setIsAuthenticated={setIsAuthenticated} />} />

            {/* Protected Routes - require authentication */}
            <Route path="/" element={
              <ProtectedRoute>
                <Home />
              </ProtectedRoute>
            } />
            <Route path="/library" element={
              <ProtectedRoute>
                <Library />
              </ProtectedRoute>
            } />
            <Route path="/planner" element={
              <ProtectedRoute>
                <Planner />
              </ProtectedRoute>
            } />
            <Route path="/active-session" element={
              <ProtectedRoute>
                <ActiveSession />
              </ProtectedRoute>
            } />
            <Route path="/stats" element={
              <ProtectedRoute>
                <Stats />
              </ProtectedRoute>
            } />
          </Routes>
        </div>

        {/* Navigation Bar - rendered on all pages */}
        <Navbar isAuthenticated={isAuthenticated} onLogout={handleLogout} />
      </div>
    </Router>
  );
}

export default App;