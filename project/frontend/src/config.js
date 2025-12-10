// File: config.js
// Author: Daniel Arteaga (d4nyart@bu.edu), 12/9/2025
// Description: Configuration file for backend API URL based on environment.

// Set API URL based on NODE_ENV (development or production)
const API_BASE_URL = process.env.NODE_ENV === 'development'
    ? 'http://127.0.0.1:8000/project/api'
    : 'https://cs-webapps.bu.edu/d4nyart/project/api';

export default API_BASE_URL;
