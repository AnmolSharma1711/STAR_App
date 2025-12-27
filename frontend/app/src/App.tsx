import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { api } from './services/api'
import type { HealthCheckResponse } from './services/api'

function App() {
  const [count, setCount] = useState(0)
  const [healthStatus, setHealthStatus] = useState<HealthCheckResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const checkHealth = async () => {
      try {
        setLoading(true)
        const response = await api.healthCheck()
        setHealthStatus(response)
        setError(null)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to connect to backend')
        setHealthStatus(null)
      } finally {
        setLoading(false)
      }
    }

    checkHealth()
    // Check health every 30 seconds
    const interval = setInterval(checkHealth, 30000)
    return () => clearInterval(interval)
  }, [])

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>TARS Club Website</h1>
      
      {/* Health Status Display */}
      <div className="card" style={{ marginBottom: '2rem' }}>
        <h2>Backend Status</h2>
        {loading ? (
          <p>Checking connection...</p>
        ) : error ? (
          <div style={{ color: '#ff6b6b' }}>
            <p>❌ Backend: Disconnected</p>
            <p style={{ fontSize: '0.9rem' }}>{error}</p>
          </div>
        ) : healthStatus ? (
          <div style={{ color: '#51cf66' }}>
            <p>✅ Backend: {healthStatus.status}</p>
            <p>✅ Database: {healthStatus.database}</p>
            <p style={{ fontSize: '0.9rem' }}>Service: {healthStatus.service}</p>
            <p style={{ fontSize: '0.8rem', opacity: 0.7 }}>
              Last checked: {new Date(healthStatus.timestamp).toLocaleTimeString()}
            </p>
          </div>
        ) : null}
        <div style={{ marginTop: '1rem' }}>
          <a 
            href="http://localhost:8000/admin/" 
            target="_blank" 
            style={{ 
              padding: '0.5rem 1rem', 
              backgroundColor: '#646cff',
              color: 'white',
              textDecoration: 'none',
              borderRadius: '8px',
              display: 'inline-block'
            }}
          >
            Open Admin Portal →
          </a>
        </div>
      </div>

      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
