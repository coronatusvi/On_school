'use client'

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react'
import { User, LoginRequest, UserCreate } from '@/lib/types'
import { apiClient } from '@/lib/api'
import { getCookie } from 'cookies-next'
import toast from 'react-hot-toast'

interface AuthContextType {
  user: User | null
  loading: boolean
  isAuthenticated: boolean
  isSeller: boolean
  isBuyer: boolean
  isAdmin: boolean
  login: (credentials: LoginRequest) => Promise<void>
  register: (userData: UserCreate) => Promise<void>
  logout: () => Promise<void>
  refreshUser: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

interface AuthProviderProps {
  children: ReactNode
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  // Computed properties
  const isAuthenticated = !!user
  const isSeller = user?.user_type === 'seller' || user?.is_superuser === true
  const isBuyer = user?.user_type === 'buyer'
  const isAdmin = user?.is_superuser === true

  // Initialize auth state
  useEffect(() => {
    checkAuthStatus()
  }, [])

  const checkAuthStatus = async () => {
    try {
      const token = getCookie('access_token')
      if (!token) {
        setLoading(false)
        return
      }

      const userData = await apiClient.getCurrentUser()
      setUser(userData)
    } catch (error) {
      // Token không hợp lệ hoặc expired
      console.error('Auth check failed:', error)
    } finally {
      setLoading(false)
    }
  }

  const login = async (credentials: LoginRequest) => {
    try {
      setLoading(true)
      const response = await apiClient.login(credentials)
      setUser(response.user)
    } catch (error) {
      throw error
    } finally {
      setLoading(false)
    }
  }

  const register = async (userData: UserCreate) => {
    try {
      setLoading(true)
      await apiClient.register(userData)
      // Sau khi đăng ký thành công, có thể tự động đăng nhập
      // hoặc redirect về trang login
    } catch (error) {
      throw error
    } finally {
      setLoading(false)
    }
  }

  const logout = async () => {
    try {
      setLoading(true)
      await apiClient.logout()
      setUser(null)
      
      // Redirect về trang chủ sau khi logout
      if (typeof window !== 'undefined') {
        window.location.href = '/'
      }
    } catch (error) {
      console.error('Logout error:', error)
      // Vẫn clear user state ngay cả khi có lỗi
      setUser(null)
    } finally {
      setLoading(false)
    }
  }

  const refreshUser = async () => {
    try {
      if (!isAuthenticated) return
      
      const userData = await apiClient.getCurrentUser()
      setUser(userData)
    } catch (error) {
      console.error('Refresh user failed:', error)
      // Nếu refresh thất bại, có thể token đã expired
      setUser(null)
    }
  }

  const contextValue: AuthContextType = {
    user,
    loading,
    isAuthenticated,
    isSeller,
    isBuyer,
    isAdmin,
    login,
    register,
    logout,
    refreshUser,
  }

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  )
}

// Custom hook để sử dụng AuthContext
export function useAuth(): AuthContextType {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

// HOC để protect routes
export function withAuth<P extends object>(
  Component: React.ComponentType<P>,
  options: {
    requireAuth?: boolean
    requireSeller?: boolean
    requireAdmin?: boolean
    redirectTo?: string
  } = {}
) {
  return function AuthenticatedComponent(props: P) {
    const { 
      isAuthenticated, 
      isSeller, 
      isAdmin, 
      loading 
    } = useAuth()
    
    const {
      requireAuth = true,
      requireSeller = false,
      requireAdmin = false,
      redirectTo = '/login'
    } = options

    useEffect(() => {
      if (loading) return

      if (requireAuth && !isAuthenticated) {
        toast.error('Vui lòng đăng nhập để truy cập trang này')
        window.location.href = redirectTo
        return
      }

      if (requireSeller && !isSeller) {
        toast.error('Bạn cần quyền người bán để truy cập trang này')
        window.location.href = '/'
        return
      }

      if (requireAdmin && !isAdmin) {
        toast.error('Bạn cần quyền admin để truy cập trang này')
        window.location.href = '/'
        return
      }
    }, [isAuthenticated, isSeller, isAdmin, loading])

    if (loading) {
      return (
        <div className="min-h-screen flex items-center justify-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
        </div>
      )
    }

    if (requireAuth && !isAuthenticated) {
      return null
    }

    if (requireSeller && !isSeller) {
      return null
    }

    if (requireAdmin && !isAdmin) {
      return null
    }

    return <Component {...props} />
  }
}

export default AuthProvider
