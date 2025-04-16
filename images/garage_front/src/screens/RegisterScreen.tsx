// @ts-ignore
import React, { useState } from 'react';
import axiosInstance from '../utilis/axiosInterceptor';

const RegisterScreen: React.FC = () => {
  const [form, setForm] = useState({
    username: '',
    email: '',
    password: '',
    confirm_password: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // @ts-ignore
    const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await axiosInstance.post('/accounts/register/', form);
      alert('Registered! Token: ' + res.data.token);
    } catch (error) {
      alert('Registration failed');
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: 100 }}>
      <h2>Register</h2>
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
        <input
          type="password"
          name="confirm_password"
          placeholder="Confirm Password"
          value={form.confirm_password}
          onChange={handleChange}
          style={{ marginBottom: 10, padding: 8, fontSize: 16 }}
          required
        />
        <button
          type="submit"
          style={{ padding: 10, backgroundColor: '#2196F3', color: 'white', border: 'none' }}
        >
          Register
        </button>
      </form>
    </div>
  );
};

export default RegisterScreen;