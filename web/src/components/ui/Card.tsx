import React from 'react'
import styles from './Card.module.css'

interface CardProps {
  children: React.ReactNode
  variant?: 'white' | 'muted' | 'primary' | 'secondary' | 'accent'
  className?: string
  onClick?: () => void
}

export function Card({ 
  children, 
  variant = 'white', 
  className = '', 
  onClick 
}: CardProps) {
  const classes = `${styles.card} ${styles[variant]} ${onClick ? styles.clickable : ''} ${className}`
  
  return (
    <div className={classes} onClick={onClick}>
      {children}
    </div>
  )
}
