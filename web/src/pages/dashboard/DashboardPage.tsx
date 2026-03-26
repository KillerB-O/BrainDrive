import { useEffect, useState } from 'react'
import axios from 'axios'
import { useAuth } from '../../context/AuthContext'
import { Card } from '../../components/ui/Card'
import { Button } from '../../components/ui/Button'
import { Input } from '../../components/ui/Input'
import { LayoutGrid, Activity, CreditCard, TrendingUp } from 'lucide-react'

interface Score {
  id: string
  score: number
  summary: string
  created_at: string
}

export function DashboardPage() {
  const { session, signOut } = useAuth()
  const [scores, setScores] = useState<Score[]>([])
  const [loading, setLoading] = useState(true)
  const [applying, setApplying] = useState(false)
  
  // Form state
  const [upiFreq, setUpiFreq] = useState('')
  const [utilityStreak, setUtilityStreak] = useState('')

  const fetchScores = async () => {
    try {
      const response = await axios.get(`${import.meta.env.VITE_API_URL}/scoring/my-scores`, {
        headers: {
          Authorization: `Bearer ${session?.access_token}`
        }
      })
      setScores(response.data)
    } catch (err) {
      console.error('Failed to fetch scores', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (session) fetchScores()
  }, [session])

  const handleApply = async (e: React.FormEvent) => {
    e.preventDefault()
    setApplying(true)
    try {
      await axios.post(`${import.meta.env.VITE_API_URL}/scoring/apply`, {
        upi_frequency: parseInt(upiFreq),
        utility_streak: parseInt(utilityStreak),
        mobile_recharges: 5 // Default for demo
      }, {
        headers: {
          Authorization: `Bearer ${session?.access_token}`
        }
      })
      fetchScores()
      setUpiFreq('')
      setUtilityStreak('')
    } catch (err) {
      console.error('Failed to apply', err)
    } finally {
      setApplying(false)
    }
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
