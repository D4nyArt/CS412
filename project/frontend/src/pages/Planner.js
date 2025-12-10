// File: Planner.js
// Author: Daniel Arteaga (d4nyart@bu.edu), 12/9/2025
// Description: Workout Planner Page.
// Allows users to create training schedules, add routines to schedules, and edit plan details.
// Features a calendar view and a drag-and-drop style builder interface.

import React, { useState, useEffect } from 'react';
import '../App.css';
import API_BASE_URL from '../config';

function Planner() {
  // State Management
  const [schedules, setSchedules] = useState([]);
  const [exercises, setExercises] = useState([]); // Store available exercises for dropdowns
  const [selectedSchedule, setSelectedSchedule] = useState(null); // If null, show list. If set, show detail.
  const [loading, setLoading] = useState(true);

  // State for Create Schedule Modal
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newScheduleData, setNewScheduleData] = useState({
    name: '',
    start_date: new Date().toISOString().split('T')[0], // Default to Today
    end_date: ''
  });

  // State for Create Routine Modal
  const [showRoutineModal, setShowRoutineModal] = useState(false);
  const [newRoutineData, setNewRoutineData] = useState({
    name: '',
    day_of_week: 'Monday'
  });

  // Staging Area for Exercises inside the Create Routine Modal
  const [pendingItems, setPendingItems] = useState([]); // List of exercises temporarily added to this routine
  const [currentItem, setCurrentItem] = useState({
    exerciseId: '',
    sets: 3,
    reps: 10
  });

  // State for Routine Detail Modal (Viewing a routine)
  const [selectedRoutineDetail, setSelectedRoutineDetail] = useState(null);

  // State for Edit Schedule Modal
  const [showEditScheduleModal, setShowEditScheduleModal] = useState(false);
  const [editScheduleData, setEditScheduleData] = useState({
    id: null,
    name: '',
    start_date: '',
    end_date: ''
  });

  // API Fetching Configuration
  const apiBaseUrl = API_BASE_URL;

  // Effect: Fetch Initial Data
  useEffect(() => {
    // We use Promise.all to fetch both schedules and exercises in parallel
    const headers = {
      'Authorization': `Token ${localStorage.getItem('token')}`,
      'X-Authorization': `Token ${localStorage.getItem('token')}`
    };
    Promise.all([
      fetch(`${apiBaseUrl}/schedules/`, { headers }).then(res => res.json()),
      fetch(`${apiBaseUrl}/exercises/`, { headers }).then(res => res.json()) // Fetch exercises
    ]).then(([schedulesData, exercisesData]) => {
      setSchedules(schedulesData);
      setExercises(exercisesData); // Store them for the dropdown
      setLoading(false);
    });
  }, [apiBaseUrl]);

  // Handlers: Schedule Management

  // Handle Form Submit to Create a new Schedule
  const handleCreateSchedule = (e) => {
    e.preventDefault(); // Stop page reload

    // Calculate is_active based on current date being within start and end dates
    const today = new Date().toISOString().split('T')[0];
    const isActive = today >= newScheduleData.start_date && today <= newScheduleData.end_date;

    // API Call to create schedule
    fetch(`${apiBaseUrl}/schedules/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${localStorage.getItem('token')}`,
        'X-Authorization': `Token ${localStorage.getItem('token')}`
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

  // Helper to add exercise to the temporary list in the modal
  const handleAddToStaging = () => {
    if (!currentItem.exerciseId) return; // Don't add if empty

    // Find the full exercise object to display the name
    const exerciseObj = exercises.find(ex => ex.id === parseInt(currentItem.exerciseId));

    const newItem = {
      ...currentItem,
      name: exerciseObj.name, // Save name for display
      tempId: Date.now() // Unique ID for React list key
    };

    setPendingItems([...pendingItems, newItem]);
    // Reset the "current item" inputs, but keep sets/reps as convenience
    setCurrentItem({ ...currentItem, exerciseId: '' });
  };

  // Handlers: Routine Management

  // Create Routine AND its Items in one go
  const handleCreateRoutine = async (e) => {
    e.preventDefault();

    try {
      // Step 1: Create the Routine Object
      const routineRes = await fetch(`${apiBaseUrl}/routines/create/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${localStorage.getItem('token')}`,
          'X-Authorization': `Token ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          schedule: selectedSchedule.id,
          name: newRoutineData.name,
          day_of_week: newRoutineData.day_of_week
        })
      });

      if (!routineRes.ok) throw new Error("Failed to create routine");
      const newRoutine = await routineRes.json();

      // Step 2: Create all the RoutineItems (Exercises)
      // We use Promise.all to do them all in parallel (Fast!)
      const itemPromises = pendingItems.map(item =>
        fetch(`${apiBaseUrl}/items/create/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('token')}`,
            'X-Authorization': `Token ${localStorage.getItem('token')}`
          },
          body: JSON.stringify({
            routine: newRoutine.id,
            exercise: item.exerciseId,
            target_sets: item.sets,
            target_reps: item.reps,
            order: 0
          })
        }).then(res => res.json())
      );

      // Wait for all items to be saved
      await Promise.all(itemPromises);

      // Step 3: Update UI state
      // We manually construct the full object to avoid another fetch
      const fullRoutine = {
        ...newRoutine,
        items: pendingItems // Attach the items we just saved
      };

      const updatedSchedule = {
        ...selectedSchedule,
        routines: [...selectedSchedule.routines, fullRoutine]
      };

      setSelectedSchedule(updatedSchedule);

      // Update main list
      const updatedSchedulesList = schedules.map(s =>
        s.id === selectedSchedule.id ? updatedSchedule : s
      );
      setSchedules(updatedSchedulesList);

      // Reset and Close Modal
      setShowRoutineModal(false);
      setNewRoutineData({ name: '', day_of_week: 'Monday' });
      setPendingItems([]); // Clear staging
    } catch (err) {
      console.error(err);
    }
  };

  // Update Schedule Details
  const handleUpdateSchedule = (e) => {
    e.preventDefault();

    const scheduleId = editScheduleData.id;
    if (!scheduleId) return;

    // Recalculate is_active
    const today = new Date().toISOString().split('T')[0];
    const isActive = today >= editScheduleData.start_date && today <= editScheduleData.end_date;

    fetch(`${apiBaseUrl}/schedules/${scheduleId}/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${localStorage.getItem('token')}`,
        'X-Authorization': `Token ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({
        name: editScheduleData.name,
        end_date: editScheduleData.end_date,
        is_active: isActive
      })
    })
      .then(res => {
        if (!res.ok) throw new Error('Failed to update');
        return res.json();
      })
      .then(updatedSchedule => {
        // Update State
        if (selectedSchedule && selectedSchedule.id === updatedSchedule.id) {
          setSelectedSchedule(updatedSchedule);
        }
        setSchedules(schedules.map(s => s.id === updatedSchedule.id ? updatedSchedule : s));
        setShowEditScheduleModal(false);
      })
      .catch(err => console.error(err));
  };

  // Helper: Generate Calendar Days
  // Renders the visual calendar grid based on the current month
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

  // VIEW 1: List of Schedules
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
              <div style={{ flex: 1 }}>
                <div className="flex-between">
                  <h3>{schedule.name}</h3>
                  <div className="flex-gap">
                    <button
                      className="btn-secondary small"
                      onClick={(e) => {
                        e.stopPropagation();
                        setEditScheduleData({
                          id: schedule.id,
                          name: schedule.name,
                          start_date: schedule.start_date,
                          end_date: schedule.end_date || ''
                        });
                        setShowEditScheduleModal(true);
                      }}
                    >
                      Edit
                    </button>
                    <button className="btn-primary small">See Details</button>
                  </div>
                </div>
                <p className="subtitle">
                  {schedule.start_date} to  {schedule.end_date || 'Ongoing'}
                  {schedule.is_active && <span style={{ color: 'var(--primary-color)', marginLeft: '10px', fontWeight: 'bold' }}> (Active)</span>}
                </p>
              </div>
            </div>
          ))}
        </div>

        {/* Modal to Create New Schedule */}
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
                    onChange={(e) => setNewScheduleData({ ...newScheduleData, name: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Start Date</label>
                  <input
                    type="date"
                    value={newScheduleData.start_date}
                    onChange={(e) => setNewScheduleData({ ...newScheduleData, start_date: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>End Date</label>
                  <input
                    type="date"
                    value={newScheduleData.end_date}
                    onChange={(e) => setNewScheduleData({ ...newScheduleData, end_date: e.target.value })}
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

        <div style={{ height: '80px' }}></div>

        {/* Modal to Edit Schedule */}
        {showEditScheduleModal && (
          <div className="modal-overlay">
            <div className="modal-content">
              <h3>Edit Plan Details</h3>
              <form onSubmit={handleUpdateSchedule}>
                <div className="form-group">
                  <label>Schedule Name</label>
                  <input
                    type="text"
                    value={editScheduleData.name}
                    onChange={(e) => setEditScheduleData({ ...editScheduleData, name: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>End Date</label>
                  <input
                    type="date"
                    value={editScheduleData.end_date}
                    onChange={(e) => setEditScheduleData({ ...editScheduleData, end_date: e.target.value })}
                    required
                  />
                </div>
                <div className="modal-actions">
                  <button type="button" className="btn-text" onClick={() => setShowEditScheduleModal(false)}>Cancel</button>
                  <button type="submit" className="btn-primary">Save Changes</button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    );
  }

  // VIEW 2: Schedule Detail (Calendar and Builder)

  const handleRoutineClick = (routine) => {
    setSelectedRoutineDetail(routine);
  };

  return (
    <div className="page-content">
      <header className="page-header">
        <button className="btn-back" onClick={() => setSelectedSchedule(null)}>← Back</button>
        <div className="flex-gap">
          <h1>{selectedSchedule.name}</h1>
        </div>
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
          <button className="btn-text" onClick={() => setShowRoutineModal(true)}>+ Add Routine</button>
        </div>

        {selectedSchedule.routines.map(routine => (
          <div
            key={routine.id}
            className="routine-row"
            onClick={() => handleRoutineClick(routine)}
            style={{ cursor: 'pointer' }}
          >
            <div className="routine-info">
              <span className="routine-day">{routine.day_of_week}</span>
              <span className="routine-name">{routine.name}</span>
            </div>
            <div className="arrow-icon">→</div>
          </div>
        ))}

        {selectedSchedule.routines.length === 0 && (
          <div className="empty-state">No routines yet. Add one!</div>
        )}
      </div>

      {/* Routine Detail Modal (Viewing Staged Items) */}
      {selectedRoutineDetail && (
        <div className="modal-overlay" onClick={() => setSelectedRoutineDetail(null)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <div className="flex-between">
              <h3>{selectedRoutineDetail.name}</h3>
              <button className="btn-text" onClick={() => setSelectedRoutineDetail(null)}>Close</button>
            </div>
            <p className="subtitle mb-2">{selectedRoutineDetail.day_of_week}</p>

            <div className="staged-list" style={{ maxHeight: '300px' }}>
              {selectedRoutineDetail.items && selectedRoutineDetail.items.length > 0 ? (
                selectedRoutineDetail.items.map((item, idx) => (
                  <div key={idx} className="staged-item">
                    <span>{item.exercise_name || item.name}</span>
                    <span className="badge-pill">
                      {item.target_sets} x {item.target_reps}
                    </span>
                  </div>
                ))
              ) : (
                <p className="text-muted">No exercises in this routine.</p>
              )}
            </div>

            <div className="modal-actions" style={{ marginTop: '20px', borderTop: '1px solid #eee', paddingTop: '15px' }}>
              <button
                className="btn-text"
                style={{ color: '#d63031' }}
                onClick={() => {
                  if (window.confirm('Are you sure you want to delete this routine?')) {
                    // Delete Logic
                    fetch(`${apiBaseUrl}/routines/${selectedRoutineDetail.id}/`, {
                      method: 'DELETE',
                      headers: {
                        'Authorization': `Token ${localStorage.getItem('token')}`,
                        'X-Authorization': `Token ${localStorage.getItem('token')}`
                      }
                    }).then(res => {
                      if (res.ok) {
                        // Remove from UI
                        const updatedRoutines = selectedSchedule.routines.filter(r => r.id !== selectedRoutineDetail.id);
                        const updatedSchedule = { ...selectedSchedule, routines: updatedRoutines };

                        setSelectedSchedule(updatedSchedule);
                        setSchedules(schedules.map(s => s.id === selectedSchedule.id ? updatedSchedule : s));

                        setSelectedRoutineDetail(null);
                      }
                    });
                  }
                }}
              >
                Delete Routine
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Routine Creation Modal */}
      {/* Allows users to add multiple exercises to a routine before saving */}
      {showRoutineModal && (
        <div className="modal-overlay">
          <div className="modal-content large"> {/* Added 'large' class for more space */}
            <h3>Design Routine</h3>
            <form onSubmit={handleCreateRoutine}>
              {/* Top Row: Name and Day */}
              <div className="form-row">
                <div className="form-group half">
                  <label>Routine Name</label>
                  <input
                    type="text"
                    placeholder="e.g. Pull Day"
                    value={newRoutineData.name}
                    onChange={e => setNewRoutineData({ ...newRoutineData, name: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group half">
                  <label>Day</label>
                  <select
                    className="form-select"
                    value={newRoutineData.day_of_week}
                    onChange={e => setNewRoutineData({ ...newRoutineData, day_of_week: e.target.value })}
                  >
                    {['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'].map(day => (
                      <option key={day} value={day}>{day}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="divider"></div>

              {/* Middle Section: Add Exercises */}
              <h4>Add Exercises</h4>
              <div className="add-exercise-box">
                <select
                  className="form-select mb-2"
                  value={currentItem.exerciseId}
                  onChange={e => setCurrentItem({ ...currentItem, exerciseId: e.target.value })}
                >
                  <option value="">Select Exercise...</option>
                  {exercises.map(ex => (
                    <option key={ex.id} value={ex.id}>{ex.name}</option>
                  ))}
                </select>

                <div className="flex-gap">
                  <input
                    type="number"
                    placeholder="Sets"
                    className="input-small"
                    value={currentItem.sets}
                    onChange={e => setCurrentItem({ ...currentItem, sets: parseInt(e.target.value) })}
                  />
                  <span className="text-muted">x</span>
                  <input
                    type="number"
                    placeholder="Reps"
                    className="input-small"
                    value={currentItem.reps}
                    onChange={e => setCurrentItem({ ...currentItem, reps: parseInt(e.target.value) })}
                  />
                  <button
                    type="button"
                    className="btn-secondary"
                    onClick={handleAddToStaging}
                    disabled={!currentItem.exerciseId}
                  >
                    Add
                  </button>
                </div>
              </div>

              {/* Bottom Section: The Staged List */}
              <div className="staged-list">
                {pendingItems.length === 0 && <p className="text-muted small">No exercises added yet.</p>}
                {pendingItems.map(item => (
                  <div key={item.tempId} className="staged-item">
                    <span>{item.name}</span>
                    <span className="badge-pill">{item.sets} x {item.reps}</span>
                  </div>
                ))}
              </div>

              <div className="modal-actions">
                <button type="button" className="btn-text" onClick={() => setShowRoutineModal(false)}>Cancel</button>
                <button type="submit" className="btn-primary">Save Routine</button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div style={{ height: '80px' }}></div>

      {/* Edit Schedule Logic Modal */}
      {showEditScheduleModal && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h3>Edit Plan Details</h3>
            <form onSubmit={handleUpdateSchedule}>
              <div className="form-group">
                <label>Schedule Name</label>
                <input
                  type="text"
                  value={editScheduleData.name}
                  onChange={(e) => setEditScheduleData({ ...editScheduleData, name: e.target.value })}
                  required
                />
              </div>
              <div className="form-group">
                <label>End Date</label>
                <input
                  type="date"
                  value={editScheduleData.end_date}
                  onChange={(e) => setEditScheduleData({ ...editScheduleData, end_date: e.target.value })}
                  required
                />
              </div>
              <div className="modal-actions">
                <button type="button" className="btn-text" onClick={() => setShowEditScheduleModal(false)}>Cancel</button>
                <button type="submit" className="btn-primary">Save Changes</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default Planner;