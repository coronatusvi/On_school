import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'
import { getCookie, setCookie, deleteCookie } from 'cookies-next'
import toast from 'react-hot-toast'
import { 
  ApiResponse, 
  LoginRequest, 
  LoginResponse, 
  UserCreate, 
  User,
  Product,
  ProductCreate,
  ProductUpdate,
  ProductListResponse,
  ProductSearch,
  StockUpdate,
  Order,
  OrderCreate,
  ReviewCreate,
  ProductReview
} from './types'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

class ApiClient {
  private api: AxiosInstance

  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 10000,
    })

    this.setupInterceptors()
  }

  private setupInterceptors() {
    // Request interceptor để thêm token
    this.api.interceptors.request.use(
      (config) => {
        const token = getCookie('access_token')
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }
        return config
      },
      (error) => {
        return Promise.reject(error)
      }
    )

    // Response interceptor để handle errors
    this.api.interceptors.response.use(
      (response: AxiosResponse) => response,
      (error) => {
        if (error.response?.status === 401) {
          this.handleUnauthorized()
        } else if (error.response?.status >= 500) {
          toast.error('Lỗi server. Vui lòng thử lại sau!')
        } else if (error.response?.data?.detail) {
          // Handle FastAPI validation errors
          if (Array.isArray(error.response.data.detail)) {
            const firstError = error.response.data.detail[0]
            toast.error(firstError.msg || 'Có lỗi xảy ra')
          } else {
            toast.error(error.response.data.detail)
          }
        } else if (error.response?.data?.message) {
          toast.error(error.response.data.message)
        }
        return Promise.reject(error)
      }
    )
  }

  private handleUnauthorized() {
    deleteCookie('access_token')
    if (typeof window !== 'undefined') {
      window.location.href = '/login'
    }
  }

  // ============================================================================
  // AUTHENTICATION METHODS
  // ============================================================================

  async login(credentials: LoginRequest): Promise<LoginResponse> {
    try {
      const response = await this.api.post<LoginResponse>('/auth/login', credentials)
      const { access_token, expires_in } = response.data
      
      // Lưu token vào cookie
      setCookie('access_token', access_token, {
        maxAge: expires_in,
        httpOnly: false,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'strict'
      })
      
      toast.success('Đăng nhập thành công!')
      return response.data
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Đăng nhập thất bại'
      toast.error(message)
      throw error
    }
  }

  async register(userData: UserCreate): Promise<User> {
    try {
      const response = await this.api.post<User>('/auth/register', userData)
      toast.success('Đăng ký thành công!')
      return response.data
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Đăng ký thất bại'
      toast.error(message)
      throw error
    }
  }

  async logout(): Promise<void> {
    try {
      await this.api.post('/auth/logout')
      deleteCookie('access_token')
      toast.success('Đăng xuất thành công!')
    } catch (error) {
      deleteCookie('access_token')
    }
  }

  async getCurrentUser(): Promise<User> {
    try {
      const response = await this.api.get<User>('/users/me')
      return response.data
    } catch (error) {
      throw error
    }
  }

  // ============================================================================
  // USER METHODS
  // ============================================================================

  async updateProfile(userData: Partial<User>): Promise<User> {
    try {
      const response = await this.api.put<User>('/users/me', userData)
      toast.success('Cập nhật profile thành công!')
      return response.data
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Cập nhật thất bại'
      toast.error(message)
      throw error
    }
  }

  // ============================================================================
  // PRODUCT METHODS
  // ============================================================================

  async getProducts(params?: {
    skip?: number
    limit?: number
    owner_id?: number
  }): Promise<ProductListResponse> {
    try {
      const response = await this.api.get<ProductListResponse>('/products/', { params })
      return response.data
    } catch (error) {
      // Trả về empty response thay vì throw error để tránh toast
      console.error('Error fetching products:', error)
      return {
        items: [],
        total: 0,
        page: 1,
        size: params?.limit || 100,
        pages: 0
      }
    }
  }

  async getProduct(id: number): Promise<Product> {
    try {
      const response = await this.api.get<Product>(`/products/${id}`)
      return response.data
    } catch (error) {
      throw error
    }
  }

  async createProduct(productData: ProductCreate): Promise<Product> {
    try {
      const response = await this.api.post<Product>('/products/', productData)
      toast.success('Tạo sản phẩm thành công!')
      return response.data
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Tạo sản phẩm thất bại'
      toast.error(message)
      throw error
    }
  }

  async updateProduct(id: number, productData: ProductUpdate): Promise<Product> {
    try {
      const response = await this.api.put<Product>(`/products/${id}`, productData)
      toast.success('Cập nhật sản phẩm thành công!')
      return response.data
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Cập nhật thất bại'
      toast.error(message)
      throw error
    }
  }

  async deleteProduct(id: number): Promise<void> {
    try {
      await this.api.delete(`/products/${id}`)
      toast.success('Xóa sản phẩm thành công!')
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Xóa sản phẩm thất bại'
      toast.error(message)
      throw error
    }
  }

  async getFeaturedProducts(limit: number = 10): Promise<Product[]> {
    try {
      const response = await this.api.get<Product[]>('/products/featured', {
        params: { limit }
      })
      return response.data
    } catch (error) {
      // Không ném lỗi để tránh hiển thị toast error
      console.error('Error fetching featured products:', error)
      return []
    }
  }

  async searchProducts(searchParams: ProductSearch, params?: {
    skip?: number
    limit?: number
  }): Promise<Product[]> {
    try {
      const response = await this.api.post<Product[]>('/products/search', searchParams, { params })
      return response.data
    } catch (error) {
      throw error
    }
  }

  async updateStock(id: number, stockUpdate: StockUpdate): Promise<Product> {
    try {
      const response = await this.api.patch<Product>(`/products/${id}/stock`, stockUpdate)
      toast.success('Cập nhật tồn kho thành công!')
      return response.data
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Cập nhật tồn kho thất bại'
      toast.error(message)
      throw error
    }
  }

  async getProductsByCategory(category: string, params?: {
    skip?: number
    limit?: number
  }): Promise<Product[]> {
    try {
      const response = await this.api.get<Product[]>(`/products/category/${category}`, { params })
      return response.data
    } catch (error) {
      throw error
    }
  }

  async getMyProducts(params?: {
    skip?: number
    limit?: number
  }): Promise<Product[]> {
    try {
      const response = await this.api.get<Product[]>('/products/my-products', { params })
      return response.data
    } catch (error) {
      throw error
    }
  }

  // ============================================================================
  // ORDER METHODS
  // ============================================================================

  async createOrder(orderData: OrderCreate): Promise<Order> {
    try {
      const response = await this.api.post<Order>('/orders/', orderData)
      toast.success('Đặt hàng thành công!')
      return response.data
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Đặt hàng thất bại'
      toast.error(message)
      throw error
    }
  }

  async getOrders(params?: {
    skip?: number
    limit?: number
    status?: string
  }): Promise<Order[]> {
    try {
      const response = await this.api.get<Order[]>('/orders/', { params })
      return response.data
    } catch (error) {
      throw error
    }
  }

  async getOrder(id: number): Promise<Order> {
    try {
      const response = await this.api.get<Order>(`/orders/${id}`)
      return response.data
    } catch (error) {
      throw error
    }
  }

  // ============================================================================
  // REVIEW METHODS
  // ============================================================================

  async createReview(reviewData: ReviewCreate): Promise<ProductReview> {
    try {
      const response = await this.api.post<ProductReview>('/reviews/', reviewData)
      toast.success('Đánh giá thành công!')
      return response.data
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Đánh giá thất bại'
      toast.error(message)
      throw error
    }
  }

  async getProductReviews(productId: number): Promise<ProductReview[]> {
    try {
      const response = await this.api.get<ProductReview[]>(`/products/${productId}/reviews`)
      return response.data
    } catch (error) {
      throw error
    }
  }

  // ============================================================================
  // UTILITY METHODS
  // ============================================================================

  async uploadImage(file: File): Promise<string> {
    try {
      const formData = new FormData()
      formData.append('file', file)
      
      const response = await this.api.post<{ url: string }>('/upload/image', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      
      return response.data.url
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Upload ảnh thất bại'
      toast.error(message)
      throw error
    }
  }

  async getCategories(): Promise<string[]> {
    try {
      const response = await this.api.get<string[]>('/categories/')
      return response.data
    } catch (error) {
      throw error
    }
  }

  // Health check
  async healthCheck(): Promise<{ status: string }> {
    try {
      const response = await this.api.get<{ status: string }>('/health')
      return response.data
    } catch (error) {
      throw error
    }
  }
}

// Export singleton instance
export const apiClient = new ApiClient()
export default apiClient
