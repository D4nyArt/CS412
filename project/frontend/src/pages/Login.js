// File: Login.js
// Author: Daniel Arteaga (d4nyart@bu.edu), 12/9/2025
// Description: Login Page.
// Authenticates user via API and stores the token in localStorage.

import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import API_BASE_URL from '../config';

const Login = ({ setIsAuthenticated }) => {
    // State for form inputs and error handling
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    // Handler for form submission
    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        try {
            // API call to get auth token
            const response = await fetch(`${API_BASE_URL}/api-token-auth/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();

            if (response.ok) {
                // Store token and user info in localStorage for session persistence
                localStorage.setItem('token', data.token);
                localStorage.setItem('user_id', data.user_id);
                localStorage.setItem('username', data.username);

                // Update app state
                setIsAuthenticated(true);

                // Redirect to home dashboard
                navigate('/');
            } else {
                setError(data.non_field_errors ? data.non_field_errors[0] : 'Login failed');
            }
        } catch (err) {
            setError('Network error. Please try again.');
        }
    };

    return (
        <div style={{ maxWidth: '400px', margin: '2rem auto', padding: '1rem', border: '1px solid #ccc', borderRadius: '8px' }}>
            <h1 style={{ textAlign: 'center', marginBottom: '1rem' }}>Welcome to FitTrack</h1>
            <h2>Login</h2>
            {error && <div style={{ color: 'red', marginBottom: '1rem' }}>{error}</div>}
            <form onSubmit={handleSubmit}>
                <div style={{ marginBottom: '1rem' }}>
                    <label style={{ display: 'block', marginBottom: '0.5rem' }}>Username:</label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        style={{ width: '100%', padding: '0.5rem' }}
                        required
                    />
                </div>
                <div style={{ marginBottom: '1rem' }}>
                    <label style={{ display: 'block', marginBottom: '0.5rem' }}>Password:</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        style={{ width: '100%', padding: '0.5rem' }}
                        required
                    />
                </div>
                <button type="submit" style={{ padding: '0.5rem 1rem', background: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                    Login
                </button>
            </form>
            <p style={{ marginTop: '1rem', textAlign: 'center' }}>
                Don't have an account? <Link to="/register">Register here</Link>
            </p>
        </div>
    );
};

export default Login;
