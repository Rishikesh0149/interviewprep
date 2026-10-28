import React, { createContext, useContext, useState, useEffect } from 'react';
import type { User } from '../types';
import { apiRequest, setAuthTokens, clearAuthTokens, getAuthToken } from '../services/api';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (data: { email: string; password: string; full_name: string; target_role?: string; experience_level?: string }) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
  deleteAccount: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const fetchCurrentUser = async () => {
    try {
      if (!getAuthToken()) {
        setUser(null);
        setLoading(false);
        return;
      }
      const data = await apiRequest<User>('/auth/me');
      setUser(data);
      localStorage.setItem('preppilot_user', JSON.stringify(data));
    } catch {
      setUser(null);
      clearAuthTokens();
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCurrentUser();

    const handleUnauthorized = () => {
      setUser(null);
    };
    window.addEventListener('auth:unauthorized', handleUnauthorized);
    return () => window.removeEventListener('auth:unauthorized', handleUnauthorized);
  }, []);

  const login = async (email: string, password: string) => {
    const data = await apiRequest<{ user: User; tokens: { access_token: string; refresh_token: string } }>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    setAuthTokens(data.tokens.access_token, data.tokens.refresh_token);
    setUser(data.user);
    localStorage.setItem('preppilot_user', JSON.stringify(data.user));
  };

  const register = async (userData: { email: string; password: string; full_name: string; target_role?: string; experience_level?: string }) => {
    const data = await apiRequest<{ user: User; tokens: { access_token: string; refresh_token: string } }>('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
    setAuthTokens(data.tokens.access_token, data.tokens.refresh_token);
    setUser(data.user);
    localStorage.setItem('preppilot_user', JSON.stringify(data.user));
  };

  const logout = () => {
    clearAuthTokens();
    setUser(null);
  };

  const deleteAccount = async () => {
    await apiRequest('/auth/account', { method: 'DELETE' });
    logout();
  };

  const refreshUser = async () => {
    await fetchCurrentUser();
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, refreshUser, deleteAccount }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
