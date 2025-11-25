import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Library from './pages/Library';
import './App.css';
import Planner from './pages/Planner';

function App() {
  return (
    <Router>
      <div className="app-container">
        <div className="content-wrap">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/library" element={<Library />} />
            <Route path="/planner" element={<Planner />} />
          </Routes>
        </div>
        <Navbar />
      </div>
    </Router>
  );
}

export default App;