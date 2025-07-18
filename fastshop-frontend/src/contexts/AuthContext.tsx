'use client'

import React, { createContext, useContext, useEffect, useState } from 'react'
import { User, LoginRequest, UserCreate } from '@/lib/types'
import { apiClient } from '@/lib/api'

interface AuthContextType {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (credentials: LoginRequest) => Promise<void>
  register: (userData: UserCreate) => Promise<void>
  logout: () => void
  isSeller: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export default function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  // Check if user has products (is seller)
  const isSeller = user !== null // For now, any logged-in user can be a seller

  const login = async (credentials: LoginRequest) => {
    try {
      setIsLoading(true)
      const response = await apiClient.login(credentials)
      
      // Store token
      if (typeof window !== 'undefined') {
        localStorage.setItem('access_token', response.access_token)
      }
      
      // Get user info
      const userInfo = await apiClient.getCurrentUser()
      setUser(userInfo)
    } catch (error) {
      console.error('Login error:', error)
      throw error
    } finally {
      setIsLoading(false)
    }
  }

  const register = async (userData: UserCreate) => {
    try {
      setIsLoading(true)
      const user = await apiClient.register(userData)
      
      // Auto login after register
      await login({
        username: userData.username,
        password: userData.password
      })
    } catch (error) {
      console.error('Register error:', error)
      throw error
    } finally {
      setIsLoading(false)
    }
  }

  const logout = () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token')
    }
    setUser(null)
  }

  // Check authentication on mount
  useEffect(() => {
    const checkAuth = async () => {
      if (typeof window === 'undefined') {
        setIsLoading(false)
        return
      }
      
      const token = localStorage.getItem('access_token')
      if (token) {
        try {
          const userInfo = await apiClient.getCurrentUser()
          setUser(userInfo)
        } catch (error) {
          if (typeof window !== 'undefined') {
            localStorage.removeItem('access_token')
          }
        }
      }
      setIsLoading(false)
    }

    checkAuth()
  }, [])

  const value: AuthContextType = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    register,
    logout,
    isSeller
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}
