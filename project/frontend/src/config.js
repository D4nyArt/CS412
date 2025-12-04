const API_BASE_URL = process.env.NODE_ENV === 'development'
    ? 'http://127.0.0.1:8000/project/api'
    : 'https://cs-webapps.bu.edu/d4nyart/project/api';

export default API_BASE_URL;
