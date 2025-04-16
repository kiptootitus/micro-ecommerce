// @ts-ignore
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosInstance from '../utilis/axiosInterceptor';

const LoginScreen: React.FC = () => {
  const [form, setForm] = useState({ email: '', password: '' });
  const navigate = useNavigate(); // hook to programmatically navigate

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // @ts-ignore
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await axiosInstance.post('/accounts/signin/', form);
      localStorage.setItem('token', res.data.token);
      alert('Logged in!');
      navigate('/'); // Redirect to homepage
    } catch (error) {
      alert('Login failed');
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: 100 }}>
      <h2>Login</h2>
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', width: 300 }}>
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={form.email}
          onChange={handleChange}
          style={{ marginBottom: 10, padding: 8, fontSize: 16 }}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={form.password}
          onChange={handleChange}
          style={{ marginBottom: 10, padding: 8, fontSize: 16 }}
          required
        />
        <button type="submit" style={{ padding: 10, backgroundColor: '#4CAF50', color: 'white', border: 'none' }}>
          Login
        </button>
      </form>
    </div>
  );
};

export default LoginScreen;
