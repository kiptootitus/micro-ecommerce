// src/api/axiosInstance.ts
import axios, { AxiosRequestConfig } from 'axios';

const baseURL = 'http://localhost:8000/';

const axiosInstance = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
});

axiosInstance.interceptors.request.use(
    //@ts-ignore
  (config: AxiosRequestConfig) => {
    const token = localStorage.getItem('access'); // JWT access token
    if (token && config.headers) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }

    if (process.env.NODE_ENV === 'development') {
      console.log(`[Axios] ${config.method?.toUpperCase()} ${config.url}`);
    }

    return config;
  },
  (error) => Promise.reject(error)
);

// Optionally handle 401 errors (e.g., token expired)
axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access');
      localStorage.removeItem('refresh');
      window.location.href = '/login'; // or route you want
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;
