// File: ActiveSession.js
// Author: Daniel Arteaga (d4nyart@bu.edu), 12/9/2025
// Description: Active Workou Session Page.
// Handles the real-time tracking of a workout, including timer and input logging (weight/reps).

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import API_BASE_URL from '../config';

function ActiveSession() {
    // State management
    const [routine, setRoutine] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [timer, setTimer] = useState(0); // Duration in seconds
    const [isActive, setIsActive] = useState(false); // Timer status
    const [logs, setLogs] = useState({}); // Stores user input: { exercise_id: { weight: '', reps: '' } }
    const navigate = useNavigate();

    // Fetch Routine on Component Mount
    useEffect(() => {
        const apiUrl = `${API_BASE_URL}/active-session/`;

        fetch(apiUrl, {
            headers: {
                'Authorization': `Token ${localStorage.getItem('token')}`,
                'X-Authorization': `Token ${localStorage.getItem('token')}`
            }
        })
            .then(async res => {
                if (!res.ok) {
                    const data = await res.json().catch(() => ({}));
                    throw new Error(data.message || 'No active session found for today');
                }
                return res.json();
            })
            .then(data => {
                setRoutine(data);
                setLoading(false);
                // Initialize logs state based on exercises in the routine
                const initialLogs = {};
                data.items.forEach(item => {
                    initialLogs[item.exercise] = { weight: '', reps: '' };
                });
                setLogs(initialLogs);
            })
            .catch(err => {
                setError(err.message);
                setLoading(false);
            });
    }, []);

    // Timer Logic: Increments every second if active
    useEffect(() => {
        let interval = null;
        if (isActive) {
            interval = setInterval(() => {
                setTimer(seconds => seconds + 1);
            }, 1000);
        } else if (!isActive && timer !== 0) {
            // Timer paused
            clearInterval(interval);
        }
        return () => clearInterval(interval);
    }, [isActive, timer]);

    // Helper to format seconds into MM:SS
    const formatTime = (seconds) => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
    };

    // Handler for input changes (Weight/Reps)
    const handleInputChange = (exerciseId, field, value) => {
        // Prevent negative values
        if (value < 0) return;

        setLogs(prev => ({
            ...prev,
            [exerciseId]: {
                ...prev[exerciseId],
                [field]: value
            }
        }));
    };

    // Submit Handler: Sends completed workout data to backend
    const handleSubmit = () => {
        const payload = {
            routine_id: routine.id,
            duration: Math.ceil(timer / 60), // Convert to minutes
            notes: "Completed via Active Session",
            // Transform logs state into array for API
            logs: Object.entries(logs).map(([exerciseId, data]) => ({
                exercise_id: exerciseId,
                weight: data.weight,
                reps: data.reps
            })).filter(log => log.weight && log.reps) // Only send completed logs
        };

        const submitUrl = `${API_BASE_URL}/submit-workout/`;

        fetch(submitUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Token ${localStorage.getItem('token')}`,
                'X-Authorization': `Token ${localStorage.getItem('token')}`
            },
            body: JSON.stringify(payload)
        })
            .then(res => {
                if (res.ok) {
                    alert('Workout Saved!');
                    navigate('/'); // Redirect to Home
                } else {
                    alert('Error saving workout');
                }
            });
    };

    // Loading State
    if (loading) return <div className="loading">Loading...</div>;

    // Error State (e.g., no routine for today)
    if (error) return (
        <div className="page-content" style={{ textAlign: 'center', marginTop: '50px' }}>
            <div className="error" style={{ color: 'red', marginBottom: '20px' }}>{error}</div>
            <button onClick={() => navigate('/')} className="btn-primary">Back to Home</button>
        </div>
    );

    return (
        <div className="active-session-container">
            <h1 className="page-title">{routine.name}</h1>

            {/* Timer Display */}
            <div className="timer-card">
                <h2 className="timer-display">{formatTime(timer)}</h2>
                <button
                    className={`timer-btn ${isActive ? 'pause' : 'start'}`}
                    onClick={() => setIsActive(!isActive)}
                >
                    {isActive ? 'PAUSE' : 'START WORKOUT'}
                </button>
            </div>

            {/* List of Exercises */}
            <div className="exercise-list">
                {routine.items.map(item => (
                    <div key={item.id} className="exercise-card">
                        <div className="exercise-header">
                            <h3>{item.exercise_name}</h3>
                            <span className="target-badge">
                                Goal: {item.target_sets} x {item.target_reps} @ {item.target_weight}lbs
                            </span>
                        </div>
                        {/* Input Fields */}
                        <div className="input-group">
                            <div className="input-wrapper">
                                <label>Weight (lbs)</label>
                                <input
                                    type="number"
                                    min="0"
                                    value={logs[item.exercise]?.weight || ''}
                                    onChange={(e) => handleInputChange(item.exercise, 'weight', e.target.value)}
                                />
                            </div>
                            <div className="input-wrapper">
                                <label>Reps</label>
                                <input
                                    type="number"
                                    min="0"
                                    value={logs[item.exercise]?.reps || ''}
                                    onChange={(e) => handleInputChange(item.exercise, 'reps', e.target.value)}
                                />
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            <button className="finish-workout-btn" onClick={handleSubmit}>
                FINISH WORKOUT
            </button>
        </div>
    );
}

export default ActiveSession;
