import React, { useState, useEffect } from 'react';
import API_BASE_URL from '../config';

function Library() {
  const [exercises, setExercises] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const apiUrl = `${API_BASE_URL}/exercises/`;

    fetch(apiUrl)
      .then(response => response.json())
      .then(data => setExercises(data))
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  const filteredExercises = exercises.filter(exercise =>
    exercise.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    exercise.muscle_group.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="page-content">
      <header className="page-header">
        <h1>Library</h1>
        <div className="control-bar">
          <input
            type="text"
            placeholder="Search..."
            className="search-input"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </header>

      <div className="exercise-grid">
        {filteredExercises.map(exercise => (
          <div key={exercise.id} className="exercise-card">
            <div className="card-header">
              <h3 className="exercise-name">{exercise.name}</h3>
              <span className={`muscle-badge badge-${exercise.muscle_group.toLowerCase()}`}>
                {exercise.muscle_group}
              </span>
            </div>
          </div>
        ))}
      </div>
      {/* Spacer for bottom nav */}
      <div style={{ height: '80px' }}></div>
    </div>
  );
}

export default Library;