import type { Metadata } from 'next'
import './globals.css'
import Image from 'next/image'

export const metadata: Metadata = {
  title: 'Phoenix Lab',
  description: 'Одностраничный веб-сайт для AI рерайта статей.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ru">
      <body>{children}</body>
    </html>
  )
}

