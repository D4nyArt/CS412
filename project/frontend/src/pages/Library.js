import React, { useState, useEffect } from 'react';
import API_BASE_URL from '../config';

function Library() {
  const [exercises, setExercises] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [newExercise, setNewExercise] = useState({ name: '', muscle_group: '' });

  useEffect(() => {
    fetchExercises();
  }, []);

  const fetchExercises = () => {
    fetch(`${API_BASE_URL}/exercises/`, {
      headers: { 'Authorization': `Token ${localStorage.getItem('token')}` }
    })
      .then(response => response.json())
      .then(data => setExercises(data))
      .catch(error => console.error('Error fetching data:', error));
  };

  const handleCreate = (e) => {
    e.preventDefault();
    fetch(`${API_BASE_URL}/exercises/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${localStorage.getItem('token')}`
      },
      body: JSON.stringify(newExercise)
    })
      .then(res => {
        if (res.ok) {
          fetchExercises();
          setShowModal(false);
          setNewExercise({ name: '', muscle_group: 'Chest' });
        }
      });
  };

  const handleDelete = (id) => {
    if (window.confirm('Delete this exercise?')) {
      fetch(`${API_BASE_URL}/exercises/${id}/`, {
        method: 'DELETE',
        headers: { 'Authorization': `Token ${localStorage.getItem('token')}` }
      }).then(res => {
        if (res.ok) fetchExercises();
      });
    }
  };

  const filteredExercises = exercises.filter(exercise =>
    exercise.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    exercise.muscle_group.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="page-content">
      <header className="page-header">
        <div className="flex-between">
          <h1>Library</h1>
          <button className="btn-primary small" onClick={() => setShowModal(true)}>+ New Exercise</button>
        </div>

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
            <button className="btn-secondary" onClick={() => handleDelete(exercise.id)} style={{ color: '#d63031', background: '#ffe6e6' }}>X</button>
          </div>
        ))}
      </div>

      {showModal && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h3>Add New Exercise</h3>
            <form onSubmit={handleCreate}>
              <div className="form-group">
                <label>Name</label>
                <input
                  type="text"
                  value={newExercise.name}
                  onChange={e => setNewExercise({ ...newExercise, name: e.target.value })}
                  required
                />
              </div>
              <div className="form-group">
                <label>Muscle Group</label>
                <input
                  type="text"
                  placeholder="e.g. Chest, Back, Legs"
                  value={newExercise.muscle_group}
                  onChange={e => setNewExercise({ ...newExercise, muscle_group: e.target.value })}
                  required
                />
              </div>
              <div className="modal-actions">
                <button type="button" className="btn-text" onClick={() => setShowModal(false)}>Cancel</button>
                <button type="submit" className="btn-primary">Save</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Spacer for bottom nav */}
      <div style={{ height: '80px' }}></div>
    </div>
  );
}

export default Library;