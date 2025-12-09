import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import '../App.css'; // Ensure global styles are imported
import API_BASE_URL from '../config';

function Home() {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  // Get today's date in a readable format (e.g., "Tuesday, Nov 21")
  const todayDisplay = new Date().toLocaleDateString('en-US', {
    weekday: 'long',
    month: 'short',
    day: 'numeric'
  });

  useEffect(() => {
    const apiUrl = `${API_BASE_URL}/dashboard/`;


    fetch(apiUrl, {
      headers: {
        'Authorization': `Token ${localStorage.getItem('token')}`
      }
    })
      .then(response => {
        if (!response.ok) {
          if (response.status === 401 || response.status === 403) {
            // Token might be invalid or expired
            localStorage.clear();
            navigate('/login');
          }
          throw new Error('Failed to fetch');
        }
        return response.json();
      })
      .then(data => {
        setDashboardData(data);
        setLoading(false);
      })
      .catch(error => console.error('Error fetching dashboard:', error));

  }, [navigate]);

  if (loading) return <div className="page-content">Loading...</div>;
  if (!dashboardData || !dashboardData.stats) return <div className="page-content">Initializing Dashboard...</div>;

  return (
    <div className="page-content">
      {/* Header Section */}
      <header className="page-header">
        <p className="subtitle">Current Trainig Shedule</p>
        <h1>{dashboardData.schedule_name}</h1>
      </header>

      {/* Dynamic Today's Card */}
      {dashboardData.today_routine ? (
        // CASE 1: It is a Workout Day
        <div className={`status-card ${dashboardData.today_routine.is_completed ? 'completed-day' : 'active-day'}`}>
          <div className="status-header">
            <h2>{todayDisplay}</h2>
            <span className="status-badge">
              {dashboardData.today_routine.is_completed ? 'Completed' : 'Scheduled'}
            </span>
          </div>
          <div className="card-body">
            <p className="status-routine">{dashboardData.today_routine.name}</p>

            {dashboardData.today_routine.is_completed ? (
              <div className="completion-message">
                <p>Great job! You've finished your workout for today.</p>
              </div>
            ) : (
              <Link to="/active-session" className="btn-primary" style={{ display: 'block', textAlign: 'center', textDecoration: 'none' }}>
                START WORKOUT
              </Link>
            )}
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

      {/* Highlights Section */}
      <h3 className="section-title" style={{ marginTop: '15px' }}>Highlights</h3>
      <div className="stats-grid">
        <div className="stat-box">
          <span className="stat-number">{dashboardData.stats.weekly_minutes}m</span>
          <span className="stat-label">Time Trained this week</span>
        </div>

        <div className="stat-box">
          {dashboardData.pr_spotlight ? (
            <>
              <span className="stat-number">{dashboardData.pr_spotlight.weight}lbs</span>
              <span className="stat-label">Best: {dashboardData.pr_spotlight.exercise}</span>
            </>
          ) : (
            <>
              <span className="stat-number">-</span>
              <span className="stat-label">No PRs yet</span>
            </>
          )}
        </div>
      </div>

      {/* Spacer for bottom nav */}
      <div style={{ height: '80px' }}></div>
    </div>
  );
}

export default Home;