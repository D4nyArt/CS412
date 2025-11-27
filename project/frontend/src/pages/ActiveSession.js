import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function ActiveSession() {
    const [routine, setRoutine] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [timer, setTimer] = useState(0);
    const [isActive, setIsActive] = useState(false);
    const [logs, setLogs] = useState({}); // { exercise_id: { weight: '', reps: '' } }
    const navigate = useNavigate();

    // Fetch Routine
    useEffect(() => {
        const apiUrl = process.env.NODE_ENV === 'development'
            ? 'http://127.0.0.1:8000/project/api/active-session/'
            : '/project/api/active-session/';

        fetch(apiUrl)
            .then(res => {
                if (!res.ok) throw new Error('No active session found for today');
                return res.json();
            })
            .then(data => {
                setRoutine(data);
                setLoading(false);
                // Initialize logs state
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

    // Timer Logic
    useEffect(() => {
        let interval = null;
        if (isActive) {
            interval = setInterval(() => {
                setTimer(seconds => seconds + 1);
            }, 1000);
        } else if (!isActive && timer !== 0) {
            clearInterval(interval);
        }
        return () => clearInterval(interval);
    }, [isActive, timer]);

    const formatTime = (seconds) => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
    };

    const handleInputChange = (exerciseId, field, value) => {
        setLogs(prev => ({
            ...prev,
            [exerciseId]: {
                ...prev[exerciseId],
                [field]: value
            }
        }));
    };

    const handleSubmit = () => {
        const payload = {
            routine_id: routine.id,
            duration: Math.ceil(timer / 60),
            notes: "Completed via Active Session",
            logs: Object.entries(logs).map(([exerciseId, data]) => ({
                exercise_id: exerciseId,
                weight: data.weight,
                reps: data.reps
            })).filter(log => log.weight && log.reps) // Only send completed logs
        };

        const submitUrl = process.env.NODE_ENV === 'development'
            ? 'http://127.0.0.1:8000/project/api/submit-workout/'
            : '/project/api/submit-workout/';

        fetch(submitUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        })
            .then(res => {
                if (res.ok) {
                    alert('Workout Saved!');
                    navigate('/');
                } else {
                    alert('Error saving workout');
                }
            });
    };

    if (loading) return <div className="loading">Loading...</div>;
    if (error) return <div className="error">{error}</div>;

    return (
        <div className="active-session-container">
            <h1 className="page-title">{routine.name}</h1>

            <div className="timer-card">
                <h2 className="timer-display">{formatTime(timer)}</h2>
                <button
                    className={`timer-btn ${isActive ? 'pause' : 'start'}`}
                    onClick={() => setIsActive(!isActive)}
                >
                    {isActive ? 'PAUSE' : 'START WORKOUT'}
                </button>
            </div>

            <div className="exercise-list">
                {routine.items.map(item => (
                    <div key={item.id} className="exercise-card">
                        <div className="exercise-header">
                            <h3>{item.exercise_name}</h3>
                            <span className="target-badge">
                                Goal: {item.target_sets} x {item.target_reps} @ {item.target_weight}lbs
                            </span>
                        </div>
                        <div className="input-group">
                            <div className="input-wrapper">
                                <label>Weight (lbs)</label>
                                <input
                                    type="number"
                                    value={logs[item.exercise]?.weight || ''}
                                    onChange={(e) => handleInputChange(item.exercise, 'weight', e.target.value)}
                                />
                            </div>
                            <div className="input-wrapper">
                                <label>Reps</label>
                                <input
                                    type="number"
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
