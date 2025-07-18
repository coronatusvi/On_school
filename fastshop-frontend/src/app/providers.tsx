'use client'

import { Toaster } from 'react-hot-toast'
import AuthProvider from '@/contexts/AuthContext'
import CartProvider from '@/contexts/CartContext'

export function Providers({ children }: { children: React.ReactNode }) {
  return (
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
  )
}
