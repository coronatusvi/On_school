// ============================================================================
// USER TYPES
// ============================================================================

export interface User {
  id: number
  username: string
  email: string
  full_name?: string
  is_active: boolean
  is_superuser: boolean
  created_at: string
  updated_at?: string
  product_count: number
  user_type: 'buyer' | 'seller' | 'admin'
}

export interface UserCreate {
  username: string
  email: string
  password: string
  full_name?: string
  user_type?: 'buyer' | 'seller'
}

export interface UserUpdate {
  email?: string
  full_name?: string
  is_active?: boolean
}

export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
  expires_in: number
  user: User
}

// ============================================================================
// PRODUCT TYPES
// ============================================================================

export type ProductStatus = 'active' | 'inactive' | 'out_of_stock' | 'discontinued'

export interface Product {
  id: number
  name: string
  description?: string
  price: number
  quantity: number
  sku: string
  category?: string
  status: ProductStatus
  is_featured: boolean
  owner_id: number
  created_at: string
  updated_at?: string
  is_available: boolean
  total_value: number
  status_display: string
  images?: ProductImage[]
  reviews?: ProductReview[]
  average_rating?: number
  review_count?: number
}

export interface ProductCreate {
  name: string
  description?: string
  price: number
  quantity: number
  sku: string
  category?: string
}

export interface ProductUpdate {
  name?: string
  description?: string
  price?: number
  quantity?: number
  category?: string
  status?: ProductStatus
  is_featured?: boolean
}

export interface ProductSearch {
  name?: string
  category?: string
  min_price?: number
  max_price?: number
  status?: ProductStatus
  is_featured?: boolean
}

export interface ProductImage {
  id: number
  product_id: number
  url: string
  alt_text?: string
  is_primary: boolean
  created_at: string
}

// ============================================================================
// REVIEW & RATING TYPES
// ============================================================================

export interface ProductReview {
  id: number
  product_id: number
  user_id: number
  user_name: string
  rating: number
  comment?: string
  created_at: string
  updated_at?: string
}

export interface ReviewCreate {
  product_id: number
  rating: number
  comment?: string
}

// ============================================================================
// CART & ORDER TYPES
// ============================================================================

export interface CartItem {
  id: string
  product: Product
  quantity: number
  price: number
  total: number
}

export interface Cart {
  items: CartItem[]
  total_items: number
  total_amount: number
}

export interface OrderItem {
  id: number
  product_id: number
  product_name: string
  product_sku: string
  quantity: number
  price: number
  total: number
}

export type OrderStatus = 'pending' | 'confirmed' | 'processing' | 'shipped' | 'delivered' | 'cancelled'

export interface Order {
  id: number
  user_id: number
  order_number: string
  status: OrderStatus
  items: OrderItem[]
  total_amount: number
  shipping_address: string
  payment_method: string
  payment_status: 'pending' | 'paid' | 'failed' | 'refunded'
  created_at: string
  updated_at?: string
  estimated_delivery?: string
}

export interface OrderCreate {
  items: Array<{
    product_id: number
    quantity: number
  }>
  shipping_address: string
  payment_method: string
}

// ============================================================================
// PAGINATION & API RESPONSE TYPES
// ============================================================================

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  size: number
  pages: number
  has_next: boolean
  has_prev: boolean
}

export interface ApiError {
  message: string
  details?: Record<string, any>
  error_type?: string
}

export interface ApiResponse<T> {
  data?: T
  error?: ApiError
  success: boolean
}

// ============================================================================
// SEARCH & FILTER TYPES
// ============================================================================

export interface SearchFilters {
  query?: string
  category?: string
  min_price?: number
  max_price?: number
  rating?: number
  in_stock?: boolean
  is_featured?: boolean
  sort_by?: 'name' | 'price' | 'rating' | 'created_at'
  sort_order?: 'asc' | 'desc'
}

export interface Category {
  id: number
  name: string
  slug: string
  description?: string
  product_count: number
  created_at: string
}

// ============================================================================
// DASHBOARD & ANALYTICS TYPES
// ============================================================================

export interface SellerStats {
  total_products: number
  active_products: number
  total_orders: number
  total_revenue: number
  pending_orders: number
  low_stock_products: number
}

export interface BuyerStats {
  total_orders: number
  total_spent: number
  favorite_products: number
  pending_orders: number
}

// ============================================================================
// FORM TYPES
// ============================================================================

export interface ContactForm {
  name: string
  email: string
  subject: string
  message: string
}

export interface PasswordChangeForm {
  current_password: string
  new_password: string
  confirm_password: string
}

// ============================================================================
// UTILITY TYPES
// ============================================================================

export type UserRole = 'buyer' | 'seller' | 'admin'
export type Theme = 'light' | 'dark'
export type NotificationType = 'success' | 'error' | 'warning' | 'info'

export interface Notification {
  id: string
  type: NotificationType
  title: string
  message: string
  duration?: number
  action?: {
    label: string
    onClick: () => void
  }
}
