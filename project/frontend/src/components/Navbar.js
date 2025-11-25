import React from 'react';
import { NavLink } from 'react-router-dom';
import './Navbar.css';

function Navbar() {
  return (
    <nav className="bottom-nav">
      <NavLink to="/" className={({ isActive }) => isActive ? "nav-item active" : "nav-item"}>
        {/* Home Icon */}
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
        <span className="nav-label">Home</span>
      </NavLink>

      <NavLink to="/library" className={({ isActive }) => isActive ? "nav-item active" : "nav-item"}>
        {/* Library/Dumbbell Icon */}
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M6.5 6.5m-2.5 0a2.5 2.5 0 1 0 5 0a2.5 2.5 0 1 0 -5 0"></path><path d="M17.5 17.5m-2.5 0a2.5 2.5 0 1 0 5 0a2.5 2.5 0 1 0 -5 0"></path><path d="M5 13l4 -8l10 0l-4 8"></path><path d="M19 11l-4 8l-10 0l4 -8"></path></svg>
        <span className="nav-label">Library</span>
      </NavLink>

      <NavLink to="/planner" className={({ isActive }) => isActive ? "nav-item active" : "nav-item"}>
          {/* Calendar Icon */}
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
          <span className="nav-label">Planner</span>
      </NavLink>
      
      {/* Placeholder for Analytics */}
      <div className="nav-item disabled">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>
        <span className="nav-label">Stats</span>
      </div>
    </nav>
  );
}

export default Navbar;