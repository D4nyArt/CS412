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


  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Check token on mount
    const token = localStorage.getItem('token');
    setIsAuthenticated(!!token);
  }, []);

  const handleLogout = () => {
    localStorage.clear();
    setIsAuthenticated(false);
    window.location.href = basename + '/login'; // Or use navigate if inside Router context, but we are outside Routes here.
    // Actually, we are inside Router, but outside Routes. To use navigate we need a wrapper or hook. 
    // Hard redirect is safe for logout to clear memory.
  };
  return (
    <Router basename={basename}>
      <div className="app-container">
        <div className="content-wrap">
          <Routes>
            <Route path="/register" element={<Register setIsAuthenticated={setIsAuthenticated} />} />
            <Route path="/login" element={<Login setIsAuthenticated={setIsAuthenticated} />} />
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
        <Navbar isAuthenticated={isAuthenticated} onLogout={handleLogout} />
      </div>
    </Router>
  );
}

export default App;