import Link from 'next/link'
import { Button } from '../components/ui/Button'

export default function HomePage() {
  return (
    <div style={{ padding: '6rem 0' }}>
      <h1 style={{ fontSize: '5rem', marginBottom: '2rem', lineHeight: 1 }}>
        CREDIT FOR <span style={{ color: 'var(--color-primary)' }}>EVERYONE.</span>
      </h1>
      <p style={{ fontSize: '1.5rem', maxWidth: '700px', marginBottom: '3rem', color: '#4B5563' }}>
        BrainDrive uses alternative data signals like UPI frequency and utility streaks 
        to build a credit profile for thin-file users. No shadows, just pure data.
      </p>
      <div style={{ display: 'flex', gap: '1.5rem' }}>
        <Link href="/signup">
          <Button size="lg">Get Scored Now</Button>
        </Link>
        <Button variant="secondary" size="lg">Learn More</Button>
      </div>
    </div>
  )
}
