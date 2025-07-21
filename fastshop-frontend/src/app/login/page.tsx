'use client'

import { useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'
import { LoginRequest } from '@/lib/types'
import { ShoppingCart, Eye, EyeOff } from 'lucide-react'

export default function LoginPage() {
  const { login, isLoading } = useAuth()
  const router = useRouter()
  const [formData, setFormData] = useState<LoginRequest>({
    username: '',
    password: ''
  })
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')

  const [validationErrors, setValidationErrors] = useState<{[key: string]: string}>({})

  const validateForm = () => {
    const errors: {[key: string]: string} = {}
    
    // Validate username
    if (!formData.username.trim()) {
      errors.username = 'Tên đăng nhập không được để trống'
    }
    // else if (formData.username.length < 3) {
    //   errors.username = 'Tên đăng nhập phải có ít nhất 3 ký tự'
    // }
    
    // Validate password
    if (!formData.password) {
      errors.password = 'Mật khẩu không được để trống'
    } 
    // else if (formData.password.length < 8) {
    //   errors.password = 'Mật khẩu phải có ít nhất 8 ký tự'
    // }
    
    setValidationErrors(errors)
    return Object.keys(errors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setValidationErrors({})

    // Validate form before submission
    if (!validateForm()) {
      return
    }

    try {
      await login(formData)
      router.push('/dashboard')
    } catch (error: any) {
      let errorMessage = 'Đăng nhập thất bại'
      
      if (error.response?.data?.detail) {
        if (Array.isArray(error.response.data.detail)) {
          // Handle Pydantic validation errors
          const validationErrors: {[key: string]: string} = {}
          error.response.data.detail.forEach((err: any) => {
            if (err.loc && err.loc.length > 0) {
              const field = err.loc[err.loc.length - 1]
              validationErrors[field] = err.msg
            }
          })
          
          if (Object.keys(validationErrors).length > 0) {
            setValidationErrors(validationErrors)
            return
          } else {
            errorMessage = error.response.data.detail[0]?.msg || errorMessage
          }
        } else if (typeof error.response.data.detail === 'string') {
          errorMessage = error.response.data.detail
        }
      }
      
      setError(errorMessage)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData({
      ...formData,
      [name]: value
    })
    
    // Clear validation error for this field when user starts typing
    if (validationErrors[name]) {
      setValidationErrors({
        ...validationErrors,
        [name]: ''
      })
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full space-y-8">
        {/* Header */}
        <div className="text-center">
          <Link href="/" className="inline-flex items-center space-x-2 mb-8">
            <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
              <ShoppingCart className="w-6 h-6 text-white" />
            </div>
            <span className="text-2xl font-bold text-gray-900">FastShop</span>
          </Link>
          <h2 className="text-3xl font-bold text-gray-900 mb-2">Đăng nhập</h2>
          <p className="text-gray-600">
            Chào mừng bạn trở lại! Vui lòng đăng nhập vào tài khoản của bạn.
          </p>
        </div>

        {/* Login Form */}
        <div className="bg-white rounded-lg shadow-sm p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
                {error}
              </div>
            )}

            <div>
              <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-2">
                Tên đăng nhập hoặc Email
              </label>
              <input
                id="username"
                name="username"
                type="text"
                required
                value={formData.username}
                onChange={handleChange}
                className={`form-input ${
                  validationErrors.username ? 'form-input-error' : ''
                }`}
                placeholder="Nhập tên đăng nhập hoặc email"
              />
              {validationErrors.username && (
                <p className="mt-1 text-sm text-red-600">{validationErrors.username}</p>
              )}
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                Mật khẩu
              </label>
              <div className="relative">
                <input
                  id="password"
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  required
                  value={formData.password}
                  onChange={handleChange}
                  className={`form-input pr-10 ${
                    validationErrors.password ? 'form-input-error' : ''
                  }`}
                  placeholder="Nhập mật khẩu"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
                >
                  {showPassword ? (
                    <EyeOff className="w-5 h-5" />
                  ) : (
                    <Eye className="w-5 h-5" />
                  )}
                </button>
              </div>
              {validationErrors.password && (
                <p className="mt-1 text-sm text-red-600">{validationErrors.password}</p>
              )}
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <input
                  id="remember"
                  name="remember"
                  type="checkbox"
                  className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                />
                <label htmlFor="remember" className="ml-2 block text-sm text-gray-700">
                  Ghi nhớ đăng nhập
                </label>
              </div>

              <div className="text-sm">
                <Link href="/forgot-password" className="text-primary-600 hover:text-primary-500">
                  Quên mật khẩu?
                </Link>
              </div>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Đang đăng nhập...' : 'Đăng nhập'}
            </button>
          </form>

          <div className="mt-6">
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-300" />
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 bg-white text-gray-500">Hoặc</span>
              </div>
            </div>

            <div className="mt-6 text-center">
              <p className="text-sm text-gray-600">
                Chưa có tài khoản?{' '}
                <Link href="/register" className="text-primary-600 hover:text-primary-500 font-medium">
                  Đăng ký ngay
                </Link>
              </p>
            </div>
          </div>
        </div>

        {/* Benefits */}
        <div className="text-center">
          <p className="text-sm text-gray-500 mb-4">
            Đăng nhập để:
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs text-gray-600">
            <div className="bg-white rounded-lg p-3 shadow-sm">
              <strong>Mua sắm</strong><br />
              Theo dõi đơn hàng & lịch sử mua hàng
            </div>
            <div className="bg-white rounded-lg p-3 shadow-sm">
              <strong>Bán hàng</strong><br />
              Quản lý sản phẩm & đơn hàng
            </div>
            <div className="bg-white rounded-lg p-3 shadow-sm">
              <strong>Tương tác</strong><br />
              Đánh giá sản phẩm & chat với người bán
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
