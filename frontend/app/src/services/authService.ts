import { Preferences } from '@capacitor/preferences';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  is_staff: boolean;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface LoginResponse {
  message: string;
  user: User;
  tokens: AuthTokens;
}

// Storage helper that uses Capacitor Preferences for mobile persistence
const storage = {
  async setItem(key: string, value: string): Promise<void> {
    try {
      await Preferences.set({ key, value });
      console.log(`[Storage] Set ${key} successfully using Preferences`);
    } catch (error) {
      console.warn(`[Storage] Preferences.set failed, using localStorage fallback:`, error);
      // Fallback to localStorage for web
      localStorage.setItem(key, value);
    }
  },

  async getItem(key: string): Promise<string | null> {
    try {
      const { value } = await Preferences.get({ key });
      console.log(`[Storage] Get ${key}:`, value ? 'found' : 'not found', 'using Preferences');
      return value;
    } catch (error) {
      console.warn(`[Storage] Preferences.get failed, using localStorage fallback:`, error);
      // Fallback to localStorage for web
      return localStorage.getItem(key);
    }
  },

  async removeItem(key: string): Promise<void> {
    try {
      await Preferences.remove({ key });
      console.log(`[Storage] Removed ${key} successfully using Preferences`);
    } catch (error) {
      console.warn(`[Storage] Preferences.remove failed, using localStorage fallback:`, error);
      // Fallback to localStorage for web
      localStorage.removeItem(key);
    }
  }
};

// Token management
export const authService = {
  // Store tokens in persistent storage
  async setTokens(tokens: AuthTokens) {
    await storage.setItem('access_token', tokens.access);
    await storage.setItem('refresh_token', tokens.refresh);
  },

  async getAccessToken(): Promise<string | null> {
    return await storage.getItem('access_token');
  },

  async getRefreshToken(): Promise<string | null> {
    return await storage.getItem('refresh_token');
  },

  async clearTokens() {
    await storage.removeItem('access_token');
    await storage.removeItem('refresh_token');
    await storage.removeItem('user');
  },

  // Store user info
  async setUser(user: User) {
    await storage.setItem('user', JSON.stringify(user));
  },

  async getUser(): Promise<User | null> {
    const userStr = await storage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  },

  // Check if user is authenticated
  async isAuthenticated(): Promise<boolean> {
    const token = await this.getAccessToken();
    return !!token;
  },

  // Login
  async login(credentials: LoginCredentials): Promise<LoginResponse> {
    const response = await fetch(`${API_BASE_URL}/api/auth/login/`, {
      method: 'POST',
      mode: 'cors',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Login failed');
    }

    const data: LoginResponse = await response.json();
    
    // Store tokens and user info
    await this.setTokens(data.tokens);
    await this.setUser(data.user);

    return data;
  },

  // Logout
  async logout(): Promise<void> {
    const refreshToken = await this.getRefreshToken();
    const accessToken = await this.getAccessToken();
    
    if (refreshToken) {
      try {
        await fetch(`${API_BASE_URL}/api/auth/logout/`, {
          method: 'POST',
          mode: 'cors',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${accessToken}`,
          },
          body: JSON.stringify({ refresh_token: refreshToken }),
        });
      } catch (error) {
        console.error('Logout error:', error);
      }
    }

    await this.clearTokens();
  },

  // Refresh access token
  async refreshToken(): Promise<string> {
    const refreshToken = await this.getRefreshToken();
    
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const response = await fetch(`${API_BASE_URL}/api/auth/token/refresh/`, {
      method: 'POST',
      mode: 'cors',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ refresh: refreshToken }),
    });

    if (!response.ok) {
      await this.clearTokens();
      throw new Error('Token refresh failed');
    }

    const data = await response.json();
    await storage.setItem('access_token', data.access);
    
    return data.access;
  },

  // Get user profile
  async getProfile(): Promise<User> {
    const token = await this.getAccessToken();
    const response = await fetch(`${API_BASE_URL}/api/auth/profile/`, {
      mode: 'cors',
      credentials: 'include',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error('Failed to fetch profile');
    }

    return response.json();
  },

  // Make authenticated request
  async fetchWithAuth(url: string, options: RequestInit = {}): Promise<Response> {
    const token = await this.getAccessToken();
    
    if (!token) {
      throw new Error('No access token available');
    }

    const response = await fetch(url, {
      ...options,
      mode: 'cors',
      credentials: 'include',
      headers: {
        ...options.headers,
        'Authorization': `Bearer ${token}`,
      },
    });

    // If token expired, try to refresh
    if (response.status === 401) {
      try {
        const newToken = await this.refreshToken();
        // Retry request with new token
        return fetch(url, {
          ...options,
          mode: 'cors',
          credentials: 'include',
          headers: {
            ...options.headers,
            'Authorization': `Bearer ${newToken}`,
          },
        });
      } catch (error) {
        await this.clearTokens();
        window.location.href = '/login';
        throw error;
      }
    }

    return response;
  },
};
