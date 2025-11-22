import React from 'react';

function Home() {
  // Mock data - later this comes from your API
  const today = new Date().toLocaleDateString('en-US', { weekday: 'long' });
  const activeSchedule = "Winter Bulk 2025";

  return (
    <div className="page-content">
      <header className="page-header">
        <p className="subtitle">Current Phase</p>
        <h1>{activeSchedule}</h1>
      </header>

      {/* Today's Status Card */}
      <div className="status-card">
        <div className="status-header">
            <h2>{today}</h2>
            <span className="status-badge">Scheduled</span>
        </div>
        <p className="status-routine">Leg Day (Hypertrophy)</p>
        <button className="btn-primary">Start Workout</button>
      </div>

      <h3 className="section-title">Quick Stats</h3>
      <div className="stats-grid">
          <div className="stat-box">
              <span className="stat-number">12</span>
              <span className="stat-label">Workouts</span>
          </div>
          <div className="stat-box">
              <span className="stat-number">3</span>
              <span className="stat-label">Streaks</span>
          </div>
      </div>
    </div>
  );
}

export default Home;