// File: ProtectedRoute.js
// Author: Daniel Arteaga (d4nyart@bu.edu), 12/9/2025
// Description: Higher-order component to protect routes that require authentication.
// Redirects unauthenticated users to the Login page.

import React from 'react';
import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ children }) => {
    // Check for authentication token in local storage
    const token = localStorage.getItem('token');

    // If no token exists, redirect to login
    if (!token) {
        return <Navigate to="/login" replace />;
    }

    // If authenticated, render the child component (the protected page)
    return children;
};

export default ProtectedRoute;
