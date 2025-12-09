import React from 'react';
import { NavLink } from 'react-router-dom';
import { Home, Dumbbell, Calendar, PlayCircle, BarChart2, LogIn, LogOut } from 'lucide-react';
import './Navbar.css';

function Navbar({ isAuthenticated, onLogout }) {
  if (!isAuthenticated) return null;

  return (
    <nav className="bottom-nav">
      <NavLink to="/" className={({ isActive }) => isActive ? "nav-item active" : "nav-item"}>
        <Home size={24} />
        <span className="nav-label">Home</span>
      </NavLink>

      <NavLink to="/library" className={({ isActive }) => isActive ? "nav-item active" : "nav-item"}>
        <Dumbbell size={24} />
        <span className="nav-label">Library</span>
      </NavLink>

      <NavLink to="/planner" className={({ isActive }) => isActive ? "nav-item active" : "nav-item"}>
        <Calendar size={24} />
        <span className="nav-label">Planner</span>
      </NavLink>

      <NavLink to="/active-session" className={({ isActive }) => isActive ? "nav-item active" : "nav-item"}>
        <PlayCircle size={24} />
        <span className="nav-label">Active</span>
      </NavLink>

      <NavLink to="/stats" className={({ isActive }) => isActive ? "nav-item active" : "nav-item"}>
        <BarChart2 size={24} />
        <span className="nav-label">Stats</span>
      </NavLink>

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