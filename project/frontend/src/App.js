import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Library from './pages/Library';
import './App.css';
import Planner from './pages/Planner';
import ActiveSession from './pages/ActiveSession';
import Stats from './pages/Stats';

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
            <Route path="/" element={<Home />} />
            <Route path="/library" element={<Library />} />
            <Route path="/planner" element={<Planner />} />
            <Route path="/active-session" element={<ActiveSession />} />
            <Route path="/stats" element={<Stats />} />
          </Routes>
        </div>
        <Navbar />
      </div>
    </Router>
  );
}

export default App;