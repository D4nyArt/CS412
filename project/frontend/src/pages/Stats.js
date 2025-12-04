import React, { useState, useEffect } from 'react';
import {
    PieChart, Pie, Cell, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
    Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
    ScatterChart, Scatter, ZAxis
} from 'recharts';
import API_BASE_URL from '../config';

function Stats() {
    const [consistencyData, setConsistencyData] = useState(null);
    const [exercises, setExercises] = useState([]);
    const [selectedExercise, setSelectedExercise] = useState('');
    const [progressionData, setProgressionData] = useState([]);
    const [muscleGroupData, setMuscleGroupData] = useState([]);
    const [scatterData, setScatterData] = useState([]);
    const [loading, setLoading] = useState(true);

    // Fetch Initial Data
    useEffect(() => {
        const fetchConsistency = async () => {
            try {
                const res = await fetch(`${API_BASE_URL}/stats/consistency/`);
                const data = await res.json();
                setConsistencyData([
                    { name: 'Completed', value: data.completed },
                    { name: 'Remaining', value: data.remaining }
                ]);
            } catch (err) { console.error(err); }
        };

        const fetchMuscleGroups = async () => {
            try {
                const res = await fetch(`${API_BASE_URL}/stats/muscle-groups/`);
                const data = await res.json();
                setMuscleGroupData(data);
            } catch (err) { console.error(err); }
        };

        const fetchExercises = async () => {
            try {
                const res = await fetch(`${API_BASE_URL}/exercises/`);
                const data = await res.json();
                setExercises(data);
                if (data.length > 0) setSelectedExercise(data[0].id);
            } catch (err) { console.error(err); }
        };

        Promise.all([fetchConsistency(), fetchMuscleGroups(), fetchExercises()]).then(() => setLoading(false));
    }, []);

    // Fetch Exercise Specific Data
    useEffect(() => {
        if (!selectedExercise) return;

        const fetchProgression = async () => {
            try {
                const res = await fetch(`${API_BASE_URL}/stats/progression/?exercise_id=${selectedExercise}`);
                const data = await res.json();
                setProgressionData(data);
            } catch (err) { console.error(err); }
        };

        const fetchScatter = async () => {
            try {
                const res = await fetch(`${API_BASE_URL}/stats/scatter/?exercise_id=${selectedExercise}`);
                const data = await res.json();
                setScatterData(data);
            } catch (err) { console.error(err); }
        };

        fetchProgression();
        fetchScatter();
    }, [selectedExercise]);

    const COLORS = ['#00b894', '#dfe6e9'];

    if (loading) return <div className="loading">Loading Stats...</div>;

    return (
        <div className="page-content">
            <header className="page-header">
                <h1>Analytics</h1>
                <p className="subtitle">Track your consistency and strength gains.</p>
            </header>

            <div className="stats-grid-2col">
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
                        <div className="legend-item"><span className="dot" style={{ background: '#00b894' }}></span> Completed</div>
                        <div className="legend-item"><span className="dot" style={{ background: '#dfe6e9' }}></span> Remaining</div>
                    </div>
                </div>

                {/* Muscle Group Radar */}
                <div className="stats-card">
                    <h3 className="section-title">Training Balance</h3>
                    <div style={{ width: '100%', height: 250 }}>
                        <ResponsiveContainer>
                            <RadarChart cx="50%" cy="50%" outerRadius="80%" data={muscleGroupData}>
                                <PolarGrid />
                                <PolarAngleAxis dataKey="subject" />
                                <PolarRadiusAxis angle={30} domain={[0, 'auto']} />
                                <Radar name="Muscle Group" dataKey="A" stroke="#6c5ce7" fill="#6c5ce7" fillOpacity={0.6} />
                                <Tooltip />
                            </RadarChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </div>

            {/* Exercise Specific Section */}
            <div className="section-header flex-between mt-4">
                <h2>Exercise Deep Dive</h2>
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

            {/* Progression Line Chart */}
            <div className="stats-card">
                <h3 className="section-title">Strength Progression</h3>
                <div style={{ width: '100%', height: 300 }}>
                    {progressionData.length > 0 ? (
                        <ResponsiveContainer>
                            <LineChart data={progressionData}>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                                <XAxis dataKey="date" tick={{ fontSize: 12 }} />
                                <YAxis />
                                <Tooltip />
                                <Line type="monotone" dataKey="weight" stroke="#0984e3" strokeWidth={3} dot={{ r: 4 }} activeDot={{ r: 6 }} />
                            </LineChart>
                        </ResponsiveContainer>
                    ) : <div className="no-data">No data yet.</div>}
                </div>
            </div>

            {/* Reps vs Weight Scatter */}
            <div className="stats-card">
                <h3 className="section-title">Intensity Zones (Reps vs Weight)</h3>
                <div style={{ width: '100%', height: 300 }}>
                    {scatterData.length > 0 ? (
                        <ResponsiveContainer>
                            <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                                <CartesianGrid />
                                <XAxis type="number" dataKey="x" name="Reps" unit="" />
                                <YAxis type="number" dataKey="y" name="Weight" unit="lbs" />
                                <ZAxis type="number" dataKey="z" range={[60, 400]} />
                                <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                                <Scatter name="Sets" data={scatterData} fill="#e17055" />
                            </ScatterChart>
                        </ResponsiveContainer>
                    ) : <div className="no-data">No data yet.</div>}
                </div>
            </div>

            <div style={{ height: '80px' }}></div>
        </div>
    );
}

export default Stats;
