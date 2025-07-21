'use client'

import { useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/contexts/AuthContext'
import { UserCreate } from '@/lib/types'
import { ShoppingCart, Eye, EyeOff, User, Store } from 'lucide-react'

export default function RegisterPage() {
  const { register, isLoading } = useAuth()
  const router = useRouter()
  const [formData, setFormData] = useState<UserCreate>({
    username: '',
    email: '',
    password: '',
    full_name: ''
  })
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [validationErrors, setValidationErrors] = useState<{[key: string]: string}>({})

  const validateUsername = (username: string): string | null => {
    if (username.length < 3) return 'Tên đăng nhập phải có ít nhất 3 ký tự'
    if (username.length > 50) return 'Tên đăng nhập không được quá 50 ký tự'
    if (!/^[a-zA-Z0-9_-]+$/.test(username)) {
      return 'Tên đăng nhập chỉ được chứa ký tự, số, dấu gạch ngang và gạch dưới'
    }
    return null
  }

  const validatePassword = (password: string): string | null => {
    if (password.length < 8) return 'Mật khẩu phải có ít nhất 8 ký tự'
    if (!/[A-Z]/.test(password)) return 'Mật khẩu phải có ít nhất 1 chữ hoa'
    if (!/[a-z]/.test(password)) return 'Mật khẩu phải có ít nhất 1 chữ thường'
    if (!/[0-9]/.test(password)) return 'Mật khẩu phải có ít nhất 1 số'
    return null
  }

  const validateEmail = (email: string): string | null => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(email)) return 'Email không hợp lệ'
    return null
  }

  const validateForm = (): boolean => {
    const errors: {[key: string]: string} = {}
    
    const usernameError = validateUsername(formData.username)
    if (usernameError) errors.username = usernameError
    
    const emailError = validateEmail(formData.email)
    if (emailError) errors.email = emailError
    
    const passwordError = validatePassword(formData.password)
    if (passwordError) errors.password = passwordError
    
    if (formData.password !== confirmPassword) {
      errors.confirmPassword = 'Mật khẩu xác nhận không khớp'
    }
    
    setValidationErrors(errors)
    return Object.keys(errors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setValidationErrors({})

    // Validate form trước khi submit
    if (!validateForm()) {
      return
    }

    try {
      await register(formData)
      router.push('/login?message=Đăng ký thành công! Vui lòng đăng nhập.')
    } catch (error: any) {
      let errorMessage = 'Đăng ký thất bại'
      
      if (error.response?.data?.detail) {
        if (Array.isArray(error.response.data.detail)) {
          // Handle Pydantic validation errors
          const fieldErrors: {[key: string]: string} = {}
          error.response.data.detail.forEach((err: any) => {
            const field = err.loc[err.loc.length - 1] // Get last element of loc array
            fieldErrors[field] = err.msg
          })
          setValidationErrors(fieldErrors)
          return
        } else if (typeof error.response.data.detail === 'string') {
          errorMessage = error.response.data.detail
        }
      }
      
      setError(errorMessage)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData({
      ...formData,
      [name]: value
    })
    
    // Clear validation error cho field đang được edit
    if (validationErrors[name]) {
      setValidationErrors({
        ...validationErrors,
        [name]: ''
      })
    }
  }

  const handleConfirmPasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setConfirmPassword(e.target.value)
    
    // Clear confirm password error
    if (validationErrors.confirmPassword) {
      setValidationErrors({
        ...validationErrors,
        confirmPassword: ''
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
          <h2 className="text-3xl font-bold text-gray-900 mb-2">Đăng ký tài khoản</h2>
          <p className="text-gray-600">
            Tạo tài khoản mới để bắt đầu mua sắm hoặc bán hàng trên FastShop
          </p>
        </div>

        {/* Register Form */}
        <div className="bg-white rounded-lg shadow-sm p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
                {error}
              </div>
            )}

            {/* Username */}
            <div>
              <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-2">
                Tên đăng nhập *
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
                placeholder="Nhập tên đăng nhập (3-50 ký tự, chỉ chữ, số, -, _)"
              />
              {validationErrors.username && (
                <p className="mt-1 text-sm text-red-600">{validationErrors.username}</p>
              )}
            </div>

            {/* Email */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                Email *
              </label>
              <input
                id="email"
                name="email"
                type="email"
                required
                value={formData.email}
                onChange={handleChange}
                className={`form-input ${
                  validationErrors.email ? 'form-input-error' : ''
                }`}
                placeholder="Nhập địa chỉ email"
              />
              {validationErrors.email && (
                <p className="mt-1 text-sm text-red-600">{validationErrors.email}</p>
              )}
            </div>

            {/* Full Name */}
            <div>
              <label htmlFor="full_name" className="block text-sm font-medium text-gray-700 mb-2">
                Họ và tên
              </label>
              <input
                id="full_name"
                name="full_name"
                type="text"
                value={formData.full_name}
                onChange={handleChange}
                className="form-input"
                placeholder="Nhập họ và tên (không bắt buộc)"
              />
            </div>

            {/* Password */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                Mật khẩu *
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
                  placeholder="Nhập mật khẩu (ít nhất 8 ký tự, có chữ hoa, thường, số)"
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

            {/* Confirm Password */}
            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-2 ">
                Xác nhận mật khẩu *
              </label>
              <input
                id="confirmPassword"
                name="confirmPassword"
                type={showPassword ? 'text' : 'password'}
                required
                value={confirmPassword}
                onChange={handleConfirmPasswordChange}
                className={'form-input'}
                placeholder="Nhập lại mật khẩu"
              />
              {validationErrors.confirmPassword && (
                <p className="mt-1 text-sm text-red-600">{validationErrors.confirmPassword}</p>
              )}
            </div> 

            <button
              type="submit"
              disabled={isLoading}
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Đang đăng ký...' : 'Đăng ký tài khoản'}
            </button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              Đã có tài khoản?{' '}
              <Link href="/login" className="text-primary-600 hover:text-primary-500 font-medium">
                Đăng nhập ngay
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
