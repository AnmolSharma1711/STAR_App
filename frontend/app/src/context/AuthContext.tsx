import { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import { authService } from '../services/authService';
import type { User } from '../services/authService';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
  // Initialize with sync check from localStorage for immediate access
  const [user, setUser] = useState<User | null>(() => {
    const storedUser = authService.getUserSync();
    console.log('[AuthProvider] Initial sync user check:', storedUser ? 'found' : 'not found');
    return storedUser;
  });
  const [isAuthenticated, setIsAuthenticated] = useState(() => authService.isAuthenticatedSync());
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is already logged in on app start
    const initializeAuth = async () => {
      try {
        // Try async check from native storage
        const storedUser = await authService.getUser();
        const token = await authService.getAccessToken();
        
        console.log('[Auth] Init - storedUser:', storedUser ? 'found' : 'not found');
        console.log('[Auth] Init - token:', token ? 'found' : 'not found');
        
        setIsAuthenticated(!!token);

        if (token) {
          // Prefer stored user; otherwise try to fetch profile. Never clear tokens on failure here.
          if (storedUser) {
            setUser(storedUser);
            console.log('[Auth] Using stored user data');
          } else {
            console.log('[Auth] Token found but no stored user');
          }

          try {
            const profile = await authService.getProfile();
            setUser(profile);
            console.log('[Auth] Profile refreshed from server');
          } catch (error) {
            console.log('[Auth] Profile fetch failed (keeping session):', error);
          }
        } else {
          console.log('[Auth] No stored token found');
        }
      } catch (error) {
        console.error('[Auth] Initialization error:', error);
        // Don't clear tokens on init error - might be temporary
      } finally {
        setLoading(false);
      }
    };

    initializeAuth();
  }, []);

  const login = async (username: string, password: string) => {
    const response = await authService.login({ username, password });
    setUser(response.user);
    setIsAuthenticated(true);
  };

  const logout = async () => {
    await authService.logout();
    setUser(null);
    setIsAuthenticated(false);
  };

  const value = {
    user,
    isAuthenticated,
    login,
    logout,
    loading,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
