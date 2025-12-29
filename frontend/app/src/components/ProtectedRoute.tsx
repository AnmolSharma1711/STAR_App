import { Navigate } from 'react-router-dom';
import { authService } from '../services/authService';
import { useState, useEffect } from 'react';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export const ProtectedRoute = ({ children }: ProtectedRouteProps) => {
  // First do a synchronous check using localStorage
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(() => {
    // Immediate sync check from localStorage
    const hasToken = authService.isAuthenticatedSync();
    console.log('[ProtectedRoute] Sync auth check:', hasToken);
    return hasToken ? true : null; // If token found, authenticated. If not, null to trigger async check
  });

  useEffect(() => {
    // If sync check didn't find token, do async check (native storage)
    if (isAuthenticated === null) {
      const checkAuth = async () => {
        const authenticated = await authService.isAuthenticated();
        console.log('[ProtectedRoute] Async auth check:', authenticated);
        setIsAuthenticated(authenticated);
      };
      checkAuth();
    }
  }, [isAuthenticated]);

  if (isAuthenticated === null) {
    // Loading state while checking authentication
    return (
      <div style={{ 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center', 
        minHeight: '100vh',
        color: 'white',
        background: '#0a0a0a'
      }}>
        <p>Loading...</p>
      </div>
    );
  }

  if (!isAuthenticated) {
    console.log('[ProtectedRoute] Not authenticated, redirecting to login');
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};
