// File: Navbar.js
// Author: Daniel Arteaga (d4nyart@bu.edu), 12/9/2025
// Description: Navigation bar component fixed at the bottom of the screen (mobile-first design).
// Provides links to main sections: Home, Library, Planner, Active Session, and Stats.

import React from 'react';
import { NavLink } from 'react-router-dom';
import { Home, Dumbbell, Calendar, PlayCircle, BarChart2, LogIn, LogOut } from 'lucide-react';
import './Navbar.css';

function Navbar({ isAuthenticated, onLogout }) {
  // If user is not logged in, do not render the navbar
  if (!isAuthenticated) return null;

  return (
    <nav className="bottom-nav">
      {/* Home Link */}
      <NavLink to="/" className={({ isActive }) => isActive ? "nav-item active" : "nav-item"}>
        <Home size={24} />
        <span className="nav-label">Home</span>
      </NavLink>

      {/* Exercise Library Link */}
      <NavLink to="/library" className={({ isActive }) => isActive ? "nav-item active" : "nav-item"}>
        <Dumbbell size={24} />
        <span className="nav-label">Library</span>
      </NavLink>

      {/* Planner/Schedule Link */}
      <NavLink to="/planner" className={({ isActive }) => isActive ? "nav-item active" : "nav-item"}>
        <Calendar size={24} />
        <span className="nav-label">Planner</span>
      </NavLink>

      {/* Active Workout Session Link */}
      <NavLink to="/active-session" className={({ isActive }) => isActive ? "nav-item active" : "nav-item"}>
        <PlayCircle size={24} />
        <span className="nav-label">Active</span>
      </NavLink>

      {/* Statistics Link */}
      <NavLink to="/stats" className={({ isActive }) => isActive ? "nav-item active" : "nav-item"}>
        <BarChart2 size={24} />
        <span className="nav-label">Stats</span>
      </NavLink>

      {/* Conditionally render Logout or Login based on auth state */}
      {isAuthenticated ? (
        <div className="nav-item" onClick={onLogout} style={{ cursor: 'pointer' }}>
          <LogOut size={24} />
          <span className="nav-label">Logout</span>
        </div>
      ) : (
        <NavLink to="/login" className={({ isActive }) => isActive ? "nav-item active" : "nav-item"}>
          <LogIn size={24} />
          <span className="nav-label">Login</span>
        </NavLink>
      )}
    </nav>
  );
}

export default Navbar;