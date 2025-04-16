// src/api/axiosInstance.ts
import axios from 'axios';

const baseURL = 'http://localhost:8000/'; // adjust if your backend uses another port

const axiosInstance = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to headers if available
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers!['Authorization'] = `Token ${token}`;
    }
    return config;
  },
    // @ts-ignore
  (error) => Promise.reject(error)
);

export default axiosInstance;
