'use client'

import React from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useAuth } from '../../context/AuthContext'
import { Button } from '../ui/Button'

interface LayoutProps {
  children: React.ReactNode
}

export function Layout({ children }: LayoutProps) {
  const { session, signOut } = useAuth()
  const pathname = usePathname()

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
          <Link href="/" style={{ textDecoration: 'none', color: 'inherit' }}>
            <div style={{ fontWeight: 800, fontSize: '1.5rem', letterSpacing: '-0.02em' }}>
              BRAIN<span style={{ color: 'var(--color-primary)' }}>DRIVE</span>
            </div>
          </Link>
          <nav>
            <ul style={{ display: 'flex', gap: '2rem', listStyle: 'none', fontWeight: 600, alignItems: 'center' }}>
              <li><Link href="/" style={{ textDecoration: 'none', color: pathname === '/' ? 'var(--color-primary)' : 'inherit' }}>Home</Link></li>
              {session ? (
                <>
                  <li><Link href="/dashboard" style={{ textDecoration: 'none', color: pathname === '/dashboard' ? 'var(--color-primary)' : 'inherit' }}>Dashboard</Link></li>
                  <li>
                    <Button 
                      variant="secondary"
                      onClick={signOut}
                      style={{ height: '3rem', padding: '0 1.5rem' }}
                    >
                      Sign Out
                    </Button>
                  </li>
                </>
              ) : (
                <>
                  <li><Link href="/login" style={{ textDecoration: 'none', color: 'inherit' }}>Login</Link></li>
                  <li>
                    <Link href="/signup">
                      <Button style={{ height: '3rem', padding: '0 1.5rem' }}>
                        Get Started
                      </Button>
                    </Link>
                  </li>
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
