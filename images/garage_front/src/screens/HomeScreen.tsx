// @ts-ignore
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosInstance from '../utilis/axiosInterceptor';

const HomeScreen: React.FC = () => {
  const [user, setUser] = useState<{ username: string; email: string } | null>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    // @ts-ignore
      const fetchUserData = async () => {
      const token = localStorage.getItem('token');
      if (!token) {
        navigate('/login');
        return;
      }

      try {
        const res = await axiosInstance.get('/accounts/me/'); // Adjust endpoint as needed
        setUser(res.data);
        setLoading(false);
      } catch (error) {
        console.error('Failed to fetch user data:', error);
        localStorage.removeItem('token');
        navigate('/login');
      }
    };

    fetchUserData();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: 100 }}>
      <h2>Welcome, {user?.username || 'User'}!</h2>
      <p>Email: {user?.email}</p>
      <button
        onClick={handleLogout}
        style={{ padding: 10, backgroundColor: '#f44336', color: 'white', border: 'none', marginTop: 20 }}
      >
        Logout
      </button>
    </div>
  );
};

export default HomeScreen;