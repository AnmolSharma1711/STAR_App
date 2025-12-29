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
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is already logged in on app start
    const initializeAuth = async () => {
      try {
        const storedUser = await authService.getUser();
        const token = await authService.getAccessToken();
        
        console.log('[Auth] Init - storedUser:', storedUser ? 'found' : 'not found');
        console.log('[Auth] Init - token:', token ? 'found' : 'not found');
        
        if (storedUser && token) {
          // Use stored user immediately - don't clear tokens on network failure
          setUser(storedUser);
          console.log('[Auth] Using stored user data');
          
          // Optionally try to refresh profile in background (don't clear on failure)
          try {
            const profile = await authService.getProfile();
            setUser(profile);
            console.log('[Auth] Profile refreshed from server');
          } catch (error) {
            // Profile fetch failed - keep using stored data, don't logout
            console.log('[Auth] Profile fetch failed, keeping stored user:', error);
          }
        } else {
          console.log('[Auth] No stored credentials found');
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
  };

  const logout = async () => {
    await authService.logout();
    setUser(null);
  };

  const value = {
    user,
    isAuthenticated: !!user,
    login,
    logout,
    loading,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
