import axios from 'axios';
// @ts-ignore
import React from 'react';

// Create an Axios instance with base configuration
const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    // Add CORS headers
    'Access-Control-Allow-Origin': '*',
  },
  withCredentials: true // Enable credentials for CORS if needed
});

// Request Interceptor
apiClient.interceptors.request.use(
  (config) => {
    // You can add authentication tokens here if needed
    // config.headers.Authorization = `Bearer ${token}`;
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    // @ts-ignore
    return Promise.reject(error);
  }
);

// Response Interceptor
apiClient.interceptors.response.use(
  (response) => {
    // Handle successful responses
    return response;
  },
  (error) => {
    // Handle errors globally
    if (error.response) {
      // Server responded with a status code outside 2xx
      console.error('Response error:', error.response.status, error.response.data);
      if (error.response.status === 401) {
        // Handle unauthorized access (e.g., redirect to login)
        alert('Session expired. Please log in again.');
      } else if (error.response.status === 403) {
        // Handle forbidden access
        alert('You do not have permission to perform this action.');
      }
    } else if (error.request) {
      // No response received
      console.error('No response received:', error.request);
      alert('Network error. Please check your connection.');
    } else {
      // Other errors
      console.error('Error:', error.message);
      alert('An unexpected error occurred.');
    }
    // @ts-ignore
    return Promise.reject(error);
  }
);

class App extends React.Component {
  state = {
    todos: [],
    loading: false,
    error: null,
  };

  componentDidMount() {
    this.fetchTodos();
  }

  // @ts-ignore
  fetchTodos = async () => {
    this.setState({ loading: true, error: null });
    try {
      const response = await apiClient.get('/todos/');
      this.setState({ todos: response.data, loading: false });
    } catch (error) {
      this.setState({ error: 'Failed to fetch todos', loading: false });
    }
  };

  render() {
    const { todos, loading, error } = this.state;

    return (
      <div className="container mx-auto p-4">
        {loading && <p>Loading...</p>}
        {error && <p className="text-red-500">{error}</p>}
        {!loading && !error && todos.length === 0 && <p>No todos found.</p>}
        <div className="space-y-2">
          {todos.map(todo => (
            <p key={todo.id} className="p-2 border rounded">
              {todo.title}
            </p>
          ))}
        </div>
      </div>
    );
  }
}

export default App;