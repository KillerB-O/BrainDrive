import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './context/AuthContext'
import { Layout } from './components/layout/Layout'
import { LoginPage } from './pages/auth/LoginPage'
import { SignupPage } from './pages/auth/SignupPage'
import { DashboardPage } from './pages/dashboard/DashboardPage'

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { session, loading } = useAuth()
  
  if (loading) return <div>Loading...</div>
  if (!session) return <Navigate to="/login" />
  
  return <>{children}</>
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Layout>
          <Routes>
            <Route path="/" element={
              <div style={{ padding: '6rem 0' }}>
                <h1 style={{ fontSize: '5rem', marginBottom: '2rem', lineHeight: 1 }}>
                  CREDIT FOR <span style={{ color: 'var(--color-primary)' }}>EVERYONE.</span>
                </h1>
                <p style={{ fontSize: '1.5rem', maxWidth: '700px', marginBottom: '3rem', color: '#4B5563' }}>
                  BrainDrive uses alternative data signals like UPI frequency and utility streaks 
                  to build a credit profile for thin-file users. No shadows, just pure data.
                </p>
                <div style={{ display: 'flex', gap: '1.5rem' }}>
                  <a href="/signup">
                    <button style={{ 
                      backgroundColor: 'var(--color-primary)', 
                      color: 'white', 
                      border: 'none', 
                      padding: '1.25rem 2.5rem', 
                      fontSize: '1.125rem', 
                      fontWeight: 700, 
                      borderRadius: 'var(--radius-md)',
                      cursor: 'pointer'
                    }}>Get Scored Now</button>
                  </a>
                  <button style={{ 
                    backgroundColor: 'var(--color-muted)', 
                    color: 'var(--color-foreground)', 
                    border: 'none', 
                    padding: '1.25rem 2.5rem', 
                    fontSize: '1.125rem', 
                    fontWeight: 700, 
                    borderRadius: 'var(--radius-md)',
                    cursor: 'pointer'
                  }}>Learn More</button>
                </div>
              </div>
            } />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/signup" element={<SignupPage />} />
            <Route path="/dashboard" element={
              <ProtectedRoute>
                <DashboardPage />
              </ProtectedRoute>
            } />
          </Routes>
        </Layout>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App
