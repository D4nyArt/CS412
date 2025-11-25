import React, { useState, useEffect } from 'react';
import '../App.css';

function Planner() {
  const [schedules, setSchedules] = useState([]);
  const [selectedSchedule, setSelectedSchedule] = useState(null); // If null, show list. If set, show detail.
  const [loading, setLoading] = useState(true);

  // State for Create Modal
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newScheduleData, setNewScheduleData] = useState({
    name: '',
    start_date: new Date().toISOString().split('T')[0], // Default to Today
    end_date: ''
  });

  // API Fetching
  const apiUrl = process.env.NODE_ENV === 'development' 
    ? 'http://127.0.0.1:8000/project/api/schedules/' 
    : '/project/api/schedules/';

  useEffect(() => {
    fetch(apiUrl)
      .then(res => res.json())
      .then(data => {
        setSchedules(data);
        setLoading(false);
      });
  }, [apiUrl]);

  // Handle Form Submit 
  const handleCreateSchedule = (e) => {
    e.preventDefault(); // Stop page reload

    // Calculate is_active based on current date being within start and end dates
    const today = new Date().toISOString().split('T')[0];
    const isActive = today >= newScheduleData.start_date && today <= newScheduleData.end_date;

    fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: newScheduleData.name,
        start_date: newScheduleData.start_date,
        end_date: newScheduleData.end_date,
        is_active: isActive
      })
    })
    .then(res => {
        if (!res.ok) throw new Error('Failed to create');
        return res.json();
    })
    .then(newSchedule => {
        // Update UI immediately (add to list)
        setSchedules([newSchedule, ...schedules]);
        // Close modal and reset form
        setShowCreateModal(false);
        setNewScheduleData({ name: '', start_date: '', end_date: '' });
    })
    .catch(err => console.error(err));
  };

  // --- Helper: Generate Calendar Days ---
  const renderCalendar = (routines) => {
    const daysInMonth = new Date(new Date().getFullYear(), new Date().getMonth() + 1, 0).getDate();
    const calendarDays = [];

    for (let i = 1; i <= daysInMonth; i++) {
      // Get specific date
      const date = new Date(new Date().getFullYear(), new Date().getMonth(), i);
      // Get day name (e.g., "Monday")
      const dayName = date.toLocaleDateString('en-US', { weekday: 'long' });
      
      // Check if any routine matches this day
      const routineForDay = routines.find(r => r.day_of_week === dayName);

      calendarDays.push(
        <div key={i} className={`calendar-day ${routineForDay ? 'has-routine' : ''}`}>
          <span className="day-number">{i}</span>
          <span className="day-name">{dayName.substring(0, 3)}</span>
          {routineForDay && (
            <div className="calendar-event-dot" title={routineForDay.name}></div>
          )}
        </div>
      );
    }
    return calendarDays;
  };

  // --- VIEW 1: List of Schedules ---
  if (!selectedSchedule) {
    return (
      <div className="page-content">
        <header className="page-header">
          <h1>My Plans</h1>
          {/* Update Button to open Modal */}
          <button 
            className="btn-primary small" 
            onClick={() => setShowCreateModal(true)}
          >
            + New Schedule
          </button>
        </header>
        
        <div className="schedule-list">
          {loading ? <p>Loading...</p> : schedules.map(schedule => (
            <div 
              key={schedule.id} 
              className={`schedule-card ${schedule.is_active ? 'active-border' : ''}`}
              onClick={() => setSelectedSchedule(schedule)}
            >
              <div>
                <h3>{schedule.name}</h3>
                <p className="subtitle">{schedule.start_date} {schedule.is_active && '(Active)'}</p>
              </div>
              <div className="arrow-icon">→</div>
            </div>
          ))}
        </div>

        {/* --- NEW: The Modal Overlay --- */}
        {showCreateModal && (
            <div className="modal-overlay">
                <div className="modal-content">
                    <h3>New Training Block</h3>
                    <form onSubmit={handleCreateSchedule}>
                        <div className="form-group">
                            <label>Schedule Name</label>
                            <input 
                                type="text" 
                                placeholder="e.g. Summer Cut 2025"
                                value={newScheduleData.name}
                                onChange={(e) => setNewScheduleData({...newScheduleData, name: e.target.value})}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label>Start Date</label>
                            <input 
                                type="date" 
                                value={newScheduleData.start_date}
                                onChange={(e) => setNewScheduleData({...newScheduleData, start_date: e.target.value})}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label>End Date</label>
                            <input 
                                type="date" 
                                value={newScheduleData.end_date}
                                onChange={(e) => setNewScheduleData({...newScheduleData, end_date: e.target.value})}
                                required
                            />
                        </div>
                        <div className="modal-actions">
                            <button type="button" className="btn-text" onClick={() => setShowCreateModal(false)}>Cancel</button>
                            <button type="submit" className="btn-primary">Create Plan</button>
                        </div>
                    </form>
                </div>
            </div>
        )}

        <div style={{height: '80px'}}></div>
      </div>
    );
  }

  // --- VIEW 2: Schedule Detail (Calendar & Builder) ---
  return (
    <div className="page-content">
      <header className="page-header">
        <button className="btn-back" onClick={() => setSelectedSchedule(null)}>← Back</button>
        <h1>{selectedSchedule.name}</h1>
      </header>

      {/* THE CALENDAR GRID */}
      <h3 className="section-title">This Month's Overview</h3>
      <div className="calendar-grid">
        {renderCalendar(selectedSchedule.routines)}
      </div>

      {/* THE BUILDER LIST */}
      <div className="routine-section">
        <div className="flex-between">
          <h3 className="section-title">Weekly Routines</h3>
          <button className="btn-text">+ Add Routine</button>
        </div>

        {selectedSchedule.routines.map(routine => (
          <div key={routine.id} className="routine-row">
            <div className="routine-info">
              <span className="routine-day">{routine.day_of_week}</span>
              <span className="routine-name">{routine.name}</span>
            </div>
            <button className="btn-icon small">+</button> 
          </div>
        ))}
        
        {selectedSchedule.routines.length === 0 && (
            <div className="empty-state">No routines yet. Add one!</div>
        )}
      </div>

      <div style={{height: '80px'}}></div>
    </div>
  );
}

export default Planner;