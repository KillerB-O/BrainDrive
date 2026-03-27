import '../styles/theme.css'
import { AuthProvider } from '../context/AuthContext'
import { Layout } from '../components/layout/Layout'

export const metadata = {
  title: 'BrainDrive - Credit for Everyone',
  description: 'Alternative credit scoring using UPI frequency and utility streaks.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          <Layout>
            {children}
          </Layout>
        </AuthProvider>
      </body>
    </html>
  )
}
