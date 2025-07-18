'use client'

import { useState, useEffect } from 'react'
import { useParams, useRouter } from 'next/navigation'
import Link from 'next/link'
import { useAuth } from '@/contexts/AuthContext'
import { apiClient } from '@/lib/api'
import { Product, ProductUpdate } from '@/lib/types'
import { 
  ArrowLeft, 
  Package, 
  DollarSign, 
  Hash, 
  FileText, 
  Tag, 
  Edit3,
  Save,
  X,
  Calendar,
  User,
  BarChart3,
  Star
} from 'lucide-react'
import toast from 'react-hot-toast'

export default function ProductDetailPage() {
  const { user, isAuthenticated } = useAuth()
  const params = useParams()
  const router = useRouter()
  const productId = parseInt(params.id as string)
  
  const [product, setProduct] = useState<Product | null>(null)
  const [loading, setLoading] = useState(true)
  const [isEditing, setIsEditing] = useState(false)
  const [saving, setSaving] = useState(false)
  const [formData, setFormData] = useState<ProductUpdate>({})
  const [errors, setErrors] = useState<Record<string, string>>({})

  useEffect(() => {
    if (isAuthenticated && productId) {
      fetchProduct()
    }
  }, [isAuthenticated, productId])

  const fetchProduct = async () => {
    try {
      setLoading(true)
      const data = await apiClient.getProduct(productId)
      setProduct(data)
      setFormData({
        name: data.name,
        description: data.description,
        price: data.price,
        quantity: data.quantity,
        category: data.category,
        status: data.status,
        is_featured: data.is_featured
      })
    } catch (error: any) {
      console.error('Fetch product error:', error)
      if (error.response?.status === 404) {
        toast.error('Không tìm thấy sản phẩm')
        router.push('/dashboard')
      } else {
        toast.error('Có lỗi xảy ra khi tải sản phẩm')
      }
    } finally {
      setLoading(false)
    }
  }

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {}

    if (!formData.name?.trim()) {
      newErrors.name = 'Tên sản phẩm là bắt buộc'
    } else if (formData.name.length < 3) {
      newErrors.name = 'Tên sản phẩm phải có ít nhất 3 ký tự'
    }

    if (formData.price !== undefined && formData.price <= 0) {
      newErrors.price = 'Giá phải lớn hơn 0'
    }

    if (formData.quantity !== undefined && formData.quantity < 0) {
      newErrors.quantity = 'Số lượng không được âm'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSave = async () => {
    if (!validateForm()) {
      return
    }

    try {
      setSaving(true)
      const updatedProduct = await apiClient.updateProduct(productId, formData)
      setProduct(updatedProduct)
      setIsEditing(false)
      toast.success('Cập nhật sản phẩm thành công!')
    } catch (error: any) {
      console.error('Update product error:', error)
      
      // Handle validation errors from backend
      if (error.response?.data?.detail && Array.isArray(error.response.data.detail)) {
        const backendErrors: Record<string, string> = {}
        error.response.data.detail.forEach((err: any) => {
          if (err.loc && err.loc.length > 1) {
            const field = err.loc[err.loc.length - 1]
            backendErrors[field] = err.msg
          }
        })
        setErrors(backendErrors)
      } else {
        toast.error('Có lỗi xảy ra khi cập nhật sản phẩm')
      }
    } finally {
      setSaving(false)
    }
  }

  const handleCancel = () => {
    if (product) {
      setFormData({
        name: product.name,
        description: product.description,
        price: product.price,
        quantity: product.quantity,
        category: product.category,
        status: product.status,
        is_featured: product.is_featured
      })
    }
    setIsEditing(false)
    setErrors({})
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target
    
    setFormData(prev => ({
      ...prev,
      [name]: type === 'number' ? parseFloat(value) || 0 : 
               type === 'checkbox' ? (e.target as HTMLInputElement).checked :
               value
    }))

    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }))
    }
  }

  const formatCurrency = (amount: number): string => {
    return new Intl.NumberFormat('vi-VN', {
      style: 'currency',
      currency: 'VND'
    }).format(amount)
  }

  const formatDate = (dateString: string): string => {
    return new Intl.DateTimeFormat('vi-VN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(new Date(dateString))
  }

  const getStatusColor = (status: string): string => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800'
      case 'inactive': return 'bg-gray-100 text-gray-800'
      case 'out_of_stock': return 'bg-red-100 text-red-800'
      case 'discontinued': return 'bg-orange-100 text-orange-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  if (!isAuthenticated) {
    router.push('/login')
    return null
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Đang tải thông tin sản phẩm...</p>
        </div>
      </div>
    )
  }

  if (!product) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Package className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Không tìm thấy sản phẩm</h2>
          <p className="text-gray-600 mb-4">Sản phẩm bạn đang tìm không tồn tại hoặc đã bị xóa.</p>
          <Link
            href="/dashboard"
            className="inline-flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Quay lại Dashboard
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <Link href="/dashboard" className="flex items-center text-gray-600 hover:text-gray-900 mr-4">
                <ArrowLeft className="w-5 h-5 mr-2" />
                Quay lại Dashboard
              </Link>
            </div>
            <div className="flex items-center space-x-4">
              {!isEditing ? (
                <button
                  onClick={() => setIsEditing(true)}
                  className="flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
                >
                  <Edit3 className="w-4 h-4 mr-2" />
                  Chỉnh sửa
                </button>
              ) : (
                <div className="flex space-x-2">
                  <button
                    onClick={handleCancel}
                    className="flex items-center px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
                  >
                    <X className="w-4 h-4 mr-2" />
                    Hủy
                  </button>
                  <button
                    onClick={handleSave}
                    disabled={saving}
                    className="flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
                  >
                    <Save className="w-4 h-4 mr-2" />
                    {saving ? 'Đang lưu...' : 'Lưu'}
                  </button>
                </div>
              )}
              <span className="text-gray-700">Xin chào, {user?.full_name || user?.username}!</span>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Product Info */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-center justify-between mb-6">
                <h1 className="text-2xl font-bold text-gray-900">Thông tin sản phẩm</h1>
                <div className="flex items-center space-x-2">
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(product.status)}`}>
                    {product.status_display}
                  </span>
                  {product.is_featured && (
                    <span className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm font-medium flex items-center">
                      <Star className="w-3 h-3 mr-1" />
                      Nổi bật
                    </span>
                  )}
                </div>
              </div>

              <div className="space-y-6">
                {/* Product Name */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    <Package className="w-4 h-4 inline mr-2" />
                    Tên sản phẩm
                  </label>
                  {isEditing ? (
                    <input
                      type="text"
                      name="name"
                      value={formData.name || ''}
                      onChange={handleChange}
                      className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 ${
                        errors.name ? 'border-red-300' : 'border-gray-300'
                      }`}
                    />
                  ) : (
                    <p className="text-lg font-medium text-gray-900">{product.name}</p>
                  )}
                  {errors.name && (
                    <p className="text-red-500 text-sm mt-1">{errors.name}</p>
                  )}
                </div>

                {/* SKU */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    <Hash className="w-4 h-4 inline mr-2" />
                    SKU
                  </label>
                  <p className="text-gray-900 font-mono bg-gray-50 px-3 py-2 rounded">{product.sku}</p>
                </div>

                {/* Price and Quantity */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      <DollarSign className="w-4 h-4 inline mr-2" />
                      Giá
                    </label>
                    {isEditing ? (
                      <input
                        type="number"
                        name="price"
                        value={formData.price || ''}
                        onChange={handleChange}
                        min="0"
                        step="1000"
                        className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 ${
                          errors.price ? 'border-red-300' : 'border-gray-300'
                        }`}
                      />
                    ) : (
                      <p className="text-lg font-bold text-primary-600">{formatCurrency(product.price)}</p>
                    )}
                    {errors.price && (
                      <p className="text-red-500 text-sm mt-1">{errors.price}</p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      <Package className="w-4 h-4 inline mr-2" />
                      Số lượng
                    </label>
                    {isEditing ? (
                      <input
                        type="number"
                        name="quantity"
                        value={formData.quantity || ''}
                        onChange={handleChange}
                        min="0"
                        className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 ${
                          errors.quantity ? 'border-red-300' : 'border-gray-300'
                        }`}
                      />
                    ) : (
                      <p className="text-lg font-medium text-gray-900">
                        {product.quantity} {product.quantity > 0 ? '(Còn hàng)' : '(Hết hàng)'}
                      </p>
                    )}
                    {errors.quantity && (
                      <p className="text-red-500 text-sm mt-1">{errors.quantity}</p>
                    )}
                  </div>
                </div>

                {/* Category */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    <Tag className="w-4 h-4 inline mr-2" />
                    Danh mục
                  </label>
                  {isEditing ? (
                    <select
                      name="category"
                      value={formData.category || ''}
                      onChange={handleChange}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                    >
                      <option value="">Chọn danh mục</option>
                      <option value="electronics">Điện tử</option>
                      <option value="fashion">Thời trang</option>
                      <option value="home">Gia dụng</option>
                      <option value="books">Sách</option>
                      <option value="sports">Thể thao</option>
                      <option value="beauty">Làm đẹp</option>
                      <option value="food">Thực phẩm</option>
                      <option value="other">Khác</option>
                    </select>
                  ) : (
                    <p className="text-gray-900">{product.category || 'Chưa phân loại'}</p>
                  )}
                </div>

                {/* Description */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    <FileText className="w-4 h-4 inline mr-2" />
                    Mô tả
                  </label>
                  {isEditing ? (
                    <textarea
                      name="description"
                      value={formData.description || ''}
                      onChange={handleChange}
                      rows={4}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                    />
                  ) : (
                    <p className="text-gray-900 whitespace-pre-wrap">
                      {product.description || 'Chưa có mô tả'}
                    </p>
                  )}
                </div>

                {/* Status and Featured (for editing) */}
                {isEditing && (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Trạng thái
                      </label>
                      <select
                        name="status"
                        value={formData.status || ''}
                        onChange={handleChange}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                      >
                        <option value="active">Hoạt động</option>
                        <option value="inactive">Tạm ngưng</option>
                        <option value="out_of_stock">Hết hàng</option>
                        <option value="discontinued">Ngừng bán</option>
                      </select>
                    </div>

                    <div className="flex items-center">
                      <input
                        type="checkbox"
                        name="is_featured"
                        checked={formData.is_featured || false}
                        onChange={handleChange}
                        className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                      />
                      <label className="ml-2 block text-sm text-gray-700">
                        Sản phẩm nổi bật
                      </label>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Statistics */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
                <BarChart3 className="w-5 h-5 mr-2" />
                Thống kê
              </h3>
              <div className="space-y-4">
                <div className="flex justify-between">
                  <span className="text-gray-600">Tổng giá trị:</span>
                  <span className="font-medium">{formatCurrency(product.total_value)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Trạng thái:</span>
                  <span className={`px-2 py-1 rounded text-xs ${getStatusColor(product.status)}`}>
                    {product.status_display}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Còn hàng:</span>
                  <span className="font-medium">{product.is_available ? 'Có' : 'Không'}</span>
                </div>
              </div>
            </div>

            {/* Metadata */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4 flex items-center">
                <Calendar className="w-5 h-5 mr-2" />
                Thông tin khác
              </h3>
              <div className="space-y-3">
                <div>
                  <span className="text-sm text-gray-600 block">Người tạo:</span>
                  <span className="text-sm font-medium flex items-center">
                    <User className="w-4 h-4 mr-1" />
                    ID: {product.owner_id}
                  </span>
                </div>
                <div>
                  <span className="text-sm text-gray-600 block">Ngày tạo:</span>
                  <span className="text-sm">{formatDate(product.created_at)}</span>
                </div>
                {product.updated_at && (
                  <div>
                    <span className="text-sm text-gray-600 block">Cập nhật lần cuối:</span>
                    <span className="text-sm">{formatDate(product.updated_at)}</span>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
