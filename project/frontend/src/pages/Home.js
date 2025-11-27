import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import '../App.css'; // Ensure global styles are imported

function Home() {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);

  // Get today's date in a readable format (e.g., "Tuesday, Nov 21")
  const todayDisplay = new Date().toLocaleDateString('en-US', {
    weekday: 'long',
    month: 'short',
    day: 'numeric'
  });

  useEffect(() => {
    const apiUrl = process.env.NODE_ENV === 'development'
      ? 'http://127.0.0.1:8000/project/api/dashboard/'
      : '/project/api/dashboard/';


    fetch(apiUrl)
      .then(response => response.json())
      .then(data => {
        setDashboardData(data);
        setLoading(false);
      })
      .catch(error => console.error('Error fetching dashboard:', error));

  }, []);

  if (loading) return <div className="page-content">Loading...</div>;

  return (
    <div className="page-content">
      {/* Header Section */}
      <header className="page-header">
        <p className="subtitle">Current Trainig Shedule</p>
        <h1>{dashboardData.schedule_name}</h1>
      </header>

      <h1>Current server time: {dashboardData.current_django_time}</h1>

      {/* Dynamic Today's Card */}
      {dashboardData.today_routine ? (
        // CASE 1: It is a Workout Day
        <div className="status-card active-day">
          <div className="status-header">
            <h2>{todayDisplay}</h2>
            <span className="status-badge">Scheduled</span>
          </div>
          <div className="card-body">
            <p className="status-routine">{dashboardData.today_routine.name}</p>
            <Link to="/active-session" className="btn-primary" style={{ display: 'block', textAlign: 'center', textDecoration: 'none' }}>
              START WORKOUT
            </Link>
          </div>
        </div>
      ) : (
        // CASE 2: It is a Rest Day
        <div className="status-card rest-day">
          <div className="status-header">
            <h2>{todayDisplay}</h2>
            <span className="status-badge rest">Rest & Recover</span>
          </div>
          <div className="card-body">
            <p className="status-routine">No workouts scheduled.</p>
            <p className="subtitle" style={{ color: '#bdc3c7' }}>Enjoy your day off!</p>
          </div>
        </div>
      )}

      {/* Quick Stats Section */}
      <h3 className="section-title">Weekly Progress</h3>
      <div className="stats-grid">
        <div className="stat-box">
          <span className="stat-number">{dashboardData.stats.completed}</span>
          <span className="stat-label">Completed</span>
        </div>

        <div className="stat-box">
          <span className="stat-number">
            {dashboardData.stats.total - dashboardData.stats.completed}
          </span>
          <span className="stat-label">Remaining</span>
        </div>
      </div>

      {/* Spacer for bottom nav */}
      <div style={{ height: '80px' }}></div>
    </div>
  );
}

export default Home;