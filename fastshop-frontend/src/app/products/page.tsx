'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useSearchParams } from 'next/navigation'
import { Product, ProductListResponse } from '@/lib/types'
import { apiClient } from '@/lib/api'
import { Package, Search, Filter, Grid, List, Star } from 'lucide-react'

export default function ProductsPage() {
  const searchParams = useSearchParams()
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [total, setTotal] = useState(0)
  const [currentPage, setCurrentPage] = useState(1)
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('')
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid')
  const [sortBy, setSortBy] = useState('created_at')
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc')

  const ITEMS_PER_PAGE = 12

  useEffect(() => {
    loadProducts()
  }, [currentPage, selectedCategory, sortBy, sortOrder])

  const loadProducts = async () => {
    try {
      setLoading(true)
      const skip = (currentPage - 1) * ITEMS_PER_PAGE
      
      const response: ProductListResponse = await apiClient.getProducts({
        skip,
        limit: ITEMS_PER_PAGE
      })
      
      setProducts(response.items)
      setTotal(response.total)
    } catch (error) {
      console.error('Error loading products:', error)
      setProducts([])
      setTotal(0)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      loadProducts()
      return
    }

    try {
      setLoading(true)
      const skip = (currentPage - 1) * ITEMS_PER_PAGE
      
      const searchResults = await apiClient.searchProducts(
        {
          name: searchQuery,
          description: searchQuery,
          category: selectedCategory || undefined
        },
        {
          skip,
          limit: ITEMS_PER_PAGE
        }
      )
      
      setProducts(searchResults)
      setTotal(searchResults.length)
    } catch (error) {
      console.error('Error searching products:', error)
      setProducts([])
      setTotal(0)
    } finally {
      setLoading(false)
    }
  }

  const handleCategoryFilter = async (category: string) => {
    try {
      setLoading(true)
      setSelectedCategory(category)
      setCurrentPage(1)
      
      if (category) {
        const categoryProducts = await apiClient.getProductsByCategory(category, {
          skip: 0,
          limit: ITEMS_PER_PAGE
        })
        setProducts(categoryProducts)
        setTotal(categoryProducts.length)
      } else {
        loadProducts()
      }
    } catch (error) {
      console.error('Error filtering by category:', error)
    } finally {
      setLoading(false)
    }
  }

  const totalPages = Math.ceil(total / ITEMS_PER_PAGE)

  const categories = [
    'Điện tử',
    'Thời trang',
    'Gia dụng',
    'Sách & Văn phòng phẩm',
    'Thể thao & Du lịch',
    'Làm đẹp & Sức khỏe',
    'Mẹ & Bé',
    'Ô tô & Xe máy'
  ]

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {[...Array(12)].map((_, index) => (
              <div key={index} className="bg-white rounded-lg shadow-sm p-4">
                <div className="w-full h-48 bg-gray-200 rounded-lg animate-pulse mb-4"></div>
                <div className="h-4 bg-gray-200 rounded animate-pulse mb-2"></div>
                <div className="h-4 bg-gray-200 rounded animate-pulse w-2/3 mb-2"></div>
                <div className="h-6 bg-gray-200 rounded animate-pulse w-1/3"></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-6">Sản phẩm</h1>
          
          {/* Search and Filters */}
          <div className="flex flex-col lg:flex-row gap-4 mb-6">
            {/* Search Bar */}
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Tìm kiếm sản phẩm..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
              <button
                onClick={handleSearch}
                className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-primary-600 text-white px-4 py-1.5 rounded-md hover:bg-primary-700 transition-colors"
              >
                Tìm
              </button>
            </div>

            {/* Category Filter */}
            <select
              value={selectedCategory}
              onChange={(e) => handleCategoryFilter(e.target.value)}
              className="px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="">Tất cả danh mục</option>
              {categories.map((category) => (
                <option key={category} value={category}>
                  {category}
                </option>
              ))}
            </select>

            {/* View Mode */}
            <div className="flex border border-gray-300 rounded-lg overflow-hidden">
              <button
                onClick={() => setViewMode('grid')}
                className={`p-3 ${viewMode === 'grid' ? 'bg-primary-600 text-white' : 'bg-white text-gray-600'}`}
              >
                <Grid className="w-5 h-5" />
              </button>
              <button
                onClick={() => setViewMode('list')}
                className={`p-3 ${viewMode === 'list' ? 'bg-primary-600 text-white' : 'bg-white text-gray-600'}`}
              >
                <List className="w-5 h-5" />
              </button>
            </div>
          </div>

          {/* Results Summary */}
          <div className="flex justify-between items-center text-sm text-gray-600">
            <span>
              Hiển thị {products.length} trong tổng số {total} sản phẩm
            </span>
            <select
              value={`${sortBy}-${sortOrder}`}
              onChange={(e) => {
                const [field, order] = e.target.value.split('-')
                setSortBy(field)
                setSortOrder(order as 'asc' | 'desc')
              }}
              className="px-3 py-1 border border-gray-300 rounded-md focus:outline-none focus:ring-1 focus:ring-primary-500"
            >
              <option value="created_at-desc">Mới nhất</option>
              <option value="created_at-asc">Cũ nhất</option>
              <option value="price-asc">Giá thấp đến cao</option>
              <option value="price-desc">Giá cao đến thấp</option>
              <option value="name-asc">Tên A-Z</option>
              <option value="name-desc">Tên Z-A</option>
            </select>
          </div>
        </div>
      </div>

      {/* Products Grid */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {products.length === 0 ? (
          <div className="text-center py-12">
            <Package className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">Không tìm thấy sản phẩm</h3>
            <p className="text-gray-600">Thử thay đổi bộ lọc hoặc từ khóa tìm kiếm</p>
          </div>
        ) : (
          <>
            <div className={
              viewMode === 'grid' 
                ? "grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
                : "space-y-4"
            }>
              {products.map((product) => (
                <ProductCard 
                  key={product.id} 
                  product={product} 
                  viewMode={viewMode}
                />
              ))}
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="mt-8 flex justify-center">
                <div className="flex space-x-2">
                  <button
                    onClick={() => setCurrentPage(currentPage - 1)}
                    disabled={currentPage === 1}
                    className="px-3 py-2 border border-gray-300 rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
                  >
                    Trước
                  </button>
                  
                  {[...Array(totalPages)].map((_, index) => {
                    const page = index + 1
                    if (
                      page === 1 || 
                      page === totalPages || 
                      (page >= currentPage - 2 && page <= currentPage + 2)
                    ) {
                      return (
                        <button
                          key={page}
                          onClick={() => setCurrentPage(page)}
                          className={`px-3 py-2 border rounded-md ${
                            page === currentPage
                              ? 'bg-primary-600 text-white border-primary-600'
                              : 'border-gray-300 hover:bg-gray-50'
                          }`}
                        >
                          {page}
                        </button>
                      )
                    } else if (
                      page === currentPage - 3 || 
                      page === currentPage + 3
                    ) {
                      return <span key={page} className="px-3 py-2">...</span>
                    }
                    return null
                  })}
                  
                  <button
                    onClick={() => setCurrentPage(currentPage + 1)}
                    disabled={currentPage === totalPages}
                    className="px-3 py-2 border border-gray-300 rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
                  >
                    Sau
                  </button>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}

interface ProductCardProps {
  product: Product
  viewMode: 'grid' | 'list'
}

function ProductCard({ product, viewMode }: ProductCardProps) {
  if (viewMode === 'list') {
    return (
      <div className="bg-white rounded-lg shadow-sm p-6 flex gap-6">
        <div className="w-32 h-32 bg-gray-200 rounded-lg flex items-center justify-center flex-shrink-0">
          <Package className="w-12 h-12 text-gray-400" />
        </div>
        
        <div className="flex-1">
          <div className="flex justify-between items-start mb-2">
            <h3 className="text-lg font-semibold text-gray-900 hover:text-primary-600">
              <Link href={`/products/${product.id}`}>
                {product.name}
              </Link>
            </h3>
            <span className={`px-2 py-1 text-xs rounded-full ${
              product.status === 'active' ? 'bg-green-100 text-green-800' :
              product.status === 'inactive' ? 'bg-gray-100 text-gray-800' :
              'bg-red-100 text-red-800'
            }`}>
              {product.status === 'active' ? 'Hoạt động' : 
               product.status === 'inactive' ? 'Tạm dừng' : 'Hết hàng'}
            </span>
          </div>
          
          <p className="text-gray-600 mb-3 line-clamp-2">
            {product.description || 'Chưa có mô tả'}
          </p>
          
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <span className="text-2xl font-bold text-primary-600">
                {product.price.toLocaleString()} ₫
              </span>
              <span className="text-sm text-gray-500">
                SKU: {product.sku}
              </span>
              <span className="text-sm text-gray-500">
                Còn lại: {product.quantity}
              </span>
            </div>
            
            <div className="flex items-center">
              <div className="flex items-center mr-2">
                {[...Array(5)].map((_, i) => (
                  <Star
                    key={i}
                    className={`w-4 h-4 ${
                      i < (product.average_rating || 0)
                        ? 'text-yellow-400 fill-current'
                        : 'text-gray-300'
                    }`}
                  />
                ))}
              </div>
              <span className="text-sm text-gray-600">
                ({product.review_count || 0})
              </span>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow p-4">
      <div className="w-full h-48 bg-gray-200 rounded-lg mb-4 flex items-center justify-center">
        <Package className="w-16 h-16 text-gray-400" />
      </div>
      
      <div className="mb-2 flex justify-between items-start">
        <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2 hover:text-primary-600">
          <Link href={`/products/${product.id}`}>
            {product.name}
          </Link>
        </h3>
        
        {product.is_featured && (
          <span className="bg-yellow-100 text-yellow-800 text-xs px-2 py-1 rounded-full">
            Nổi bật
          </span>
        )}
      </div>
      
      <p className="text-gray-600 text-sm mb-3 line-clamp-2">
        {product.description || 'Chưa có mô tả'}
      </p>
      
      <div className="flex items-center mb-3">
        <div className="flex items-center">
          {[...Array(5)].map((_, i) => (
            <Star
              key={i}
              className={`w-4 h-4 ${
                i < (product.average_rating || 0)
                  ? 'text-yellow-400 fill-current'
                  : 'text-gray-300'
              }`}
            />
          ))}
        </div>
        <span className="text-sm text-gray-600 ml-2">
          ({product.review_count || 0})
        </span>
      </div>
      
      <div className="flex items-center justify-between mb-3">
        <span className="text-primary-600 font-bold text-lg">
          {product.price.toLocaleString()} ₫
        </span>
        <span className="text-sm text-gray-500">
          Còn: {product.quantity}
        </span>
      </div>
      
      <Link
        href={`/products/${product.id}`}
        className="block w-full bg-primary-600 text-white text-center py-2 rounded-lg hover:bg-primary-700 transition-colors"
      >
        Xem chi tiết
      </Link>
    </div>
  )
}
