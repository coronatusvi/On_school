import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { Toaster } from 'react-hot-toast'
import AuthProvider from '@/contexts/AuthContext'
import CartProvider from '@/contexts/CartContext'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'FastShop - Nền tảng thương mại điện tử',
  description: 'Mua sắm trực tuyến dễ dàng với FastShop. Hàng nghìn sản phẩm chất lượng, giao hàng nhanh chóng.',
  keywords: 'mua sắm, thương mại điện tử, online shopping, fastshop',
  authors: [{ name: 'FastShop Team' }],
  viewport: 'width=device-width, initial-scale=1',
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
        <AuthProvider>
          <CartProvider>
            <div className="flex flex-col min-h-screen">
              {/* Main content */}
              <main className="flex-grow">
                {children}
              </main>
            </div>

            {/* Toast notifications */}
            <Toaster
              position="top-right"
              reverseOrder={false}
              gutter={8}
              containerClassName=""
              containerStyle={{}}
              toastOptions={{
                // Default options for all toasts
                className: '',
                duration: 4000,
                style: {
                  background: '#363636',
                  color: '#fff',
                },

                // Success toast style
                success: {
                  duration: 3000,
                  style: {
                    background: '#10B981',
                    color: '#fff',
                  },
                  iconTheme: {
                    primary: '#fff',
                    secondary: '#10B981',
                  },
                },

                // Error toast style
                error: {
                  duration: 5000,
                  style: {
                    background: '#EF4444',
                    color: '#fff',
                  },
                  iconTheme: {
                    primary: '#fff',
                    secondary: '#EF4444',
                  },
                },
              }}
            />
          </CartProvider>
        </AuthProvider>
      </body>
    </html>
  )
}
