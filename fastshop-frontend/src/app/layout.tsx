import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { Providers } from './providers'

const inter = Inter({ subsets: ['latin'] })

// Export viewport separately (NextJS 14+ requirement)
export const viewport = {
  width: 'device-width',
  initialScale: 1,
}

export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000'),
  title: 'FastShop - Nền tảng thương mại điện tử',
  description: 'Mua sắm trực tuyến dễ dàng với FastShop. Hàng nghìn sản phẩm chất lượng, giao hàng nhanh chóng.',
  keywords: 'mua sắm, thương mại điện tử, online shopping, fastshop',
  authors: [{ name: 'FastShop Team' }],
  robots: 'index, follow',
  openGraph: {
    title: 'FastShop - Nền tảng thương mại điện tử',
    description: 'Mua sắm trực tuyến dễ dàng với FastShop',
    type: 'website',
    locale: 'vi_VN',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="vi" className={inter.className}>
      <head>
        <link rel="icon" href="/favicon.ico" />
        <meta name="theme-color" content="#3B82F6" />
      </head>
      <body className="min-h-screen bg-gray-50">
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  )
}
