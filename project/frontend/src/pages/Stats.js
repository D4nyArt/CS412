import React, { useState, useEffect } from 'react';
import { PieChart, Pie, Cell, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

function Stats() {
    const [consistencyData, setConsistencyData] = useState(null);
    const [exercises, setExercises] = useState([]);
    const [selectedExercise, setSelectedExercise] = useState('');
    const [progressionData, setProgressionData] = useState([]);
    const [loading, setLoading] = useState(true);

    // Fetch Consistency Data & Exercise List
    useEffect(() => {
        const fetchConsistency = async () => {
            const apiUrl = process.env.NODE_ENV === 'development'
                ? 'http://127.0.0.1:8000/project/api/stats/consistency/'
                : '/project/api/stats/consistency/';

            try {
                const res = await fetch(apiUrl);
                const data = await res.json();
                setConsistencyData([
                    { name: 'Completed', value: data.completed },
                    { name: 'Remaining', value: data.remaining }
                ]);
            } catch (err) {
                console.error("Error fetching consistency:", err);
            }
        };

        const fetchExercises = async () => {
            const apiUrl = process.env.NODE_ENV === 'development'
                ? 'http://127.0.0.1:8000/project/api/exercises/'
                : '/project/api/exercises/';

            try {
                const res = await fetch(apiUrl);
                const data = await res.json();
                setExercises(data);
                if (data.length > 0) setSelectedExercise(data[0].id);
            } catch (err) {
                console.error("Error fetching exercises:", err);
            }
        };

        Promise.all([fetchConsistency(), fetchExercises()]).then(() => setLoading(false));
    }, []);

    // Fetch Progression Data when exercise changes
    useEffect(() => {
        if (!selectedExercise) return;

        const fetchProgression = async () => {
            const apiUrl = process.env.NODE_ENV === 'development'
                ? `http://127.0.0.1:8000/project/api/stats/progression/?exercise_id=${selectedExercise}`
                : `/project/api/stats/progression/?exercise_id=${selectedExercise}`;

            try {
                const res = await fetch(apiUrl);
                const data = await res.json();
                setProgressionData(data);
            } catch (err) {
                console.error("Error fetching progression:", err);
            }
        };

        fetchProgression();
    }, [selectedExercise]);

    const COLORS = ['#00b894', '#dfe6e9'];

    if (loading) return <div className="loading">Loading Stats...</div>;

    return (
        <div className="page-content">
            <header className="page-header">
                <h1>Analytics</h1>
                <p className="subtitle">Track your consistency and strength gains.</p>
            </header>

            {/* Consistency Section */}
            <div className="stats-card">
                <h3 className="section-title">Schedule Consistency</h3>
                <div style={{ width: '100%', height: 250 }}>
                    <ResponsiveContainer>
                        <PieChart>
                            <Pie
                                data={consistencyData}
                                cx="50%"
                                cy="50%"
                                innerRadius={60}
                                outerRadius={80}
                                fill="#8884d8"
                                paddingAngle={5}
                                dataKey="value"
                            >
                                {consistencyData.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                ))}
                            </Pie>
                            <Tooltip />
                        </PieChart>
                    </ResponsiveContainer>
                </div>
                <div className="legend">
                    <div className="legend-item">
                        <span className="dot" style={{ background: '#00b894' }}></span> Completed
                    </div>
                    <div className="legend-item">
                        <span className="dot" style={{ background: '#dfe6e9' }}></span> Remaining
                    </div>
                </div>
            </div>

            {/* Progression Section */}
            <div className="stats-card">
                <div className="flex-between">
                    <h3 className="section-title">Strength Progression</h3>
                    <select
                        className="form-select"
                        style={{ width: 'auto' }}
                        value={selectedExercise}
                        onChange={(e) => setSelectedExercise(e.target.value)}
                    >
                        {exercises.map(ex => (
                            <option key={ex.id} value={ex.id}>{ex.name}</option>
                        ))}
                    </select>
                </div>

                <div style={{ width: '100%', height: 300 }}>
                    {progressionData.length > 0 ? (
                        <ResponsiveContainer>
                            <LineChart data={progressionData}>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                                <XAxis dataKey="date" tick={{ fontSize: 12 }} />
                                <YAxis />
                                <Tooltip />
                                <Line
                                    type="monotone"
                                    dataKey="weight"
                                    stroke="#0984e3"
                                    strokeWidth={3}
                                    dot={{ r: 4 }}
                                    activeDot={{ r: 6 }}
                                />
                            </LineChart>
                        </ResponsiveContainer>
                    ) : (
                        <div className="no-data">No data for this exercise yet.</div>
                    )}
                </div>
            </div>

            <div style={{ height: '80px' }}></div>
        </div>
    );
}

export default Stats;
