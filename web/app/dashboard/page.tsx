'use client'

import { useEffect, useState, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '../../context/AuthContext'
import { Card } from '../../components/ui/Card'
import { Button } from '../../components/ui/Button'
import { Input } from '../../components/ui/Input'

interface Score {
  id: string
  score: number
  summary: string
  created_at: string
}

export default function DashboardPage() {
  const { session, loading: authLoading, signOut } = useAuth()
  const router = useRouter()
  const [scores, setScores] = useState<Score[]>([])
  const [loading, setLoading] = useState(true)
  const [applying, setApplying] = useState(false)
  const [error, setError] = useState<string | null>(null)
  
  // Form state
  const [upiFreq, setUpiFreq] = useState('')
  const [utilityStreak, setUtilityStreak] = useState('')

  const fetchScores = useCallback(async () => {
    if (!session?.access_token) return
    setError(null)
    try {
      setLoading(true)
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'
      const response = await fetch(`${apiUrl}/scoring/my-scores`, {
        headers: {
          'Authorization': `Bearer ${session.access_token}`,
          'Content-Type': 'application/json'
        }
      })
      
      if (!response.ok) {
        let errorMsg = `Error ${response.status}`
        try {
          const errorJson = await response.json()
          errorMsg = errorJson.detail || JSON.stringify(errorJson)
        } catch {
          errorMsg = await response.text() || errorMsg
        }
        console.error('Backend Error:', response.status, errorMsg);
        setError(`Failed to fetch scores: ${errorMsg}`);
        return
      }
      
      const data = await response.json()
      setScores(data)
    } catch (err) {
      console.error('Failed to fetch scores', err)
      setError('Network error: Failed to connect to backend.')
    } finally {
      setLoading(false)
    }
  }, [session])

  useEffect(() => {
    if (!authLoading && !session) {
      router.replace('/login')
    }
  }, [session, authLoading, router])

  useEffect(() => {
    if (session) fetchScores()
  }, [session, fetchScores])

  const handleApply = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!session?.access_token) return

    setApplying(true)
    setError(null)
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'
      const response = await fetch(`${apiUrl}/scoring/apply`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${session.access_token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          monthly_upi_txn_count: parseInt(upiFreq),
          utility_payment_streak: parseInt(utilityStreak),
          avg_monthly_inflow: 50000,
          mobile_recharge_freq: 5,
          gst_filed: false,
          rental_payment_months: 12,
          employment_type: 'salaried',
          years_at_address: 2.5
        })
      })

      if (!response.ok) {
        let errorMsg = `Error ${response.status}`
        try {
          const errorJson = await response.json()
          errorMsg = errorJson.detail || JSON.stringify(errorJson)
        } catch {
          errorMsg = await response.text() || errorMsg
        }
        throw new Error(errorMsg)
      }
      
      await fetchScores()
      setUpiFreq('')
      setUtilityStreak('')
    } catch (err: any) {
      console.error('Failed to apply', err)
      setError(`Application failed: ${err.message}`)
    } finally {
      setApplying(false)
    }
  }

  if (authLoading || !session) {
    return <div style={{ padding: '4rem 0' }}>Loading session...</div>
  }

  return (
    <div style={{ padding: '2rem 0' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '3rem' }}>
        <div>
          <h1 style={{ fontSize: '3rem' }}>Dashboard</h1>
          <p style={{ color: '#6B7280' }}>Manage your alternative credit profile.</p>
        </div>
        <Button variant="secondary" onClick={signOut}>Sign Out</Button>
      </div>

      {error && (
        <Card variant="muted" style={{ backgroundColor: '#FEE2E2', borderColor: '#EF4444', marginBottom: '2rem' }}>
          <p style={{ color: '#B91C1C' }}>{error}</p>
        </Card>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '2rem' }}>
        {/* Application Form */}
        <Card variant="white">
          <h3 style={{ fontSize: '1.5rem', marginBottom: '1.5rem' }}>Update Data</h3>
          <form onSubmit={handleApply} style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
            <Input 
              label="Monthly UPI Frequency" 
              type="number" 
              value={upiFreq}
              onChange={(e) => setUpiFreq(e.target.value)}
              placeholder="e.g. 45"
              required
            />
            <Input 
              label="Utility Payment Streak (Months)" 
              type="number" 
              value={utilityStreak}
              onChange={(e) => setUtilityStreak(e.target.value)}
              placeholder="e.g. 12"
              required
            />
            <Button type="submit" disabled={applying}>
              {applying ? 'Calculating...' : 'Calculate Score'}
            </Button>
          </form>
        </Card>

        {/* Score History */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <h3 style={{ fontSize: '1.5rem' }}>Your Score History</h3>
          {loading ? (
            <p>Loading scores...</p>
          ) : scores.length === 0 ? (
            <Card variant="muted">
              <p>No scores yet. Apply above to generate your first credit score!</p>
            </Card>
          ) : (
            scores.map((s) => (
              <Card key={s.id} variant="white" className="card-hover">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
                    <div style={{ 
                      backgroundColor: 'var(--color-primary)', 
                      color: 'white', 
                      width: '4rem', 
                      height: '4rem', 
                      borderRadius: 'var(--radius-md)', 
                      display: 'flex', 
                      justifyContent: 'center', 
                      alignItems: 'center',
                      fontSize: '1.5rem',
                      fontWeight: 800
                    }}>
                      {s.score}
                    </div>
                    <div>
                      <h4 style={{ fontSize: '1.25rem' }}>Credit Score</h4>
                      <p style={{ color: '#6B7280' }}>Generated on {new Date(s.created_at).toLocaleDateString()}</p>
                    </div>
                  </div>
                  <div style={{ textAlign: 'right', maxWidth: '300px' }}>
                    <p style={{ fontSize: '0.875rem', color: '#4B5563' }}>{s.summary}</p>
                  </div>
                </div>
              </Card>
            ))
          )}
        </div>
      </div>
      
      {/* Decorative Geometric Shapes */}
      <div style={{ 
        position: 'fixed', 
        bottom: '-100px', 
        right: '-100px', 
        width: '400px', 
        height: '400px', 
        backgroundColor: 'var(--color-primary)', 
        opacity: 0.05, 
        borderRadius: '50%', 
        zIndex: -1 
      }} />
      <div style={{ 
        position: 'fixed', 
        top: '20%', 
        left: '-50px', 
        width: '200px', 
        height: '200px', 
        backgroundColor: 'var(--color-secondary)', 
        opacity: 0.05, 
        transform: 'rotate(45deg)', 
        zIndex: -1 
      }} />
    </div>
  )
}
