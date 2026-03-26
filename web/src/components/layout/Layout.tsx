import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'

interface LayoutProps {
  children: React.ReactNode
}

export function Layout({ children }: LayoutProps) {
  const { session, signOut } = useAuth()
  const location = useLocation()

  return (
    <div>
      <header style={{ 
        padding: '1.5rem 0', 
        borderBottom: '2px solid var(--color-border)',
        backgroundColor: 'var(--color-background)',
        position: 'sticky',
        top: 0,
        zIndex: 10
      }}>
        <div className="container" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
            <div style={{ fontWeight: 800, fontSize: '1.5rem', letterSpacing: '-0.02em' }}>
              BRAIN<span style={{ color: 'var(--color-primary)' }}>DRIVE</span>
            </div>
          </Link>
          <nav>
            <ul style={{ display: 'flex', gap: '2rem', listStyle: 'none', fontWeight: 600, alignItems: 'center' }}>
              <li><Link to="/" style={{ textDecoration: 'none', color: location.pathname === '/' ? 'var(--color-primary)' : 'inherit' }}>Home</Link></li>
              {session ? (
                <>
                  <li><Link to="/dashboard" style={{ textDecoration: 'none', color: location.pathname === '/dashboard' ? 'var(--color-primary)' : 'inherit' }}>Dashboard</Link></li>
                  <li>
                    <button 
                      onClick={signOut}
                      style={{ 
                        background: 'none', 
                        border: 'none', 
                        cursor: 'pointer', 
                        fontWeight: 600, 
                        fontFamily: 'inherit',
                        color: '#6B7280'
                      }}
                    >
                      Sign Out
                    </button>
                  </li>
                </>
              ) : (
                <>
                  <li><Link to="/login" style={{ textDecoration: 'none', color: 'inherit' }}>Login</Link></li>
                  <li><Link to="/signup" style={{ 
                    textDecoration: 'none', 
                    backgroundColor: 'var(--color-primary)', 
                    color: 'white',
                    padding: '0.75rem 1.5rem',
                    borderRadius: 'var(--radius-md)',
                    transition: 'all 200ms',
                    display: 'inline-block'
                  }}>Get Started</Link></li>
                </>
              )}
            </ul>
          </nav>
        </div>
      </header>
      <main className="container">
        {children}
      </main>
    </div>
  )
}
