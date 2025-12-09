import React from 'react';
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

  return (
    <Router basename={basename}>
      <div className="app-container">
        <div className="content-wrap">
          <Routes>
            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login />} />
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
        <Navbar />
      </div>
    </Router>
  );
}

export default App;