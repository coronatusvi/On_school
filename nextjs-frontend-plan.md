# 🛒 E-Commerce Platform - NextJS Frontend

## 🎯 Ứng dụng Business: Marketplace Bán Hàng Online

### Concept: **"FastShop" - Nền tảng thương mại điện tử**
- **Người bán (Seller)**: Đăng ký tài khoản, tạo shop, quản lý sản phẩm, theo dõi đơn hàng
- **Người mua (Buyer)**: Duyệt sản phẩm, thêm vào giỏ hàng, đặt hàng, thanh toán
- **Admin**: Quản lý users, sản phẩm, đơn hàng, thống kê

### Core Features:
1. **Multi-vendor marketplace** - Nhiều người bán trên cùng platform
2. **Shopping cart & checkout** - Giỏ hàng và thanh toán
3. **Order management** - Quản lý đơn hàng
4. **Product reviews & ratings** - Đánh giá sản phẩm
5. **Search & filter** - Tìm kiếm nâng cao
6. **Seller dashboard** - Bảng điều khiển người bán

## 🏗️ System Architecture

### User Roles & Permissions:
```
┌─ Anonymous User ─┐    ┌─ Buyer ─┐    ┌─ Seller ─┐    ┌─ Admin ─┐
│ • Browse products│    │ • Login │    │ • Login  │    │ • Full   │
│ • View details   │────│ • Buy   │────│ • Sell   │────│ Access  │
│ • Register       │    │ • Review│    │ • Manage │    │ • Manage│
└───────────────────┘    └─────────┘    └──────────┘    └─────────┘
```

### App Flow:
```
Landing Page → Browse Products → Product Detail → Add to Cart
     ↓              ↓              ↓              ↓
Register/Login → Search/Filter → Reviews → Checkout → Payment
     ↓
User Dashboard → Order History → Seller Dashboard (if seller)
```

## 📋 Kịch bản Implementation

### Phase 1: Khởi tạo và Setup (30-45 phút)
```bash
# 1. Tạo NextJS project
npx create-next-app@latest fastapi-frontend --typescript --tailwind --eslint --app

# 2. Cài đặt dependencies
npm install axios react-hook-form @hookform/resolvers zod
npm install @types/node @types/react @types/react-dom
npm install lucide-react react-hot-toast
npm install js-cookie @types/js-cookie

# 3. Cấu hình môi trường
# Tạo .env.local với API_URL
```

### Phase 2: Cấu trúc Project (15-20 phút)
```
src/
├── app/                    # App Router (NextJS 13+)
│   ├── globals.css
│   ├── layout.tsx
│   ├── page.tsx           # Home page
│   ├── login/
│   │   └── page.tsx       # Login page
│   ├── register/
│   │   └── page.tsx       # Register page
│   ├── dashboard/
│   │   └── page.tsx       # User dashboard
│   └── products/
│       ├── page.tsx       # Products list
│       ├── [id]/
│       │   └── page.tsx   # Product detail
│       └── create/
│           └── page.tsx   # Create product
├── components/
│   ├── ui/                # Reusable UI components
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Card.tsx
│   │   └── Modal.tsx
│   ├── forms/             # Form components
│   │   ├── LoginForm.tsx
│   │   ├── RegisterForm.tsx
│   │   └── ProductForm.tsx
│   ├── layout/            # Layout components
│   │   ├── Header.tsx
│   │   ├── Sidebar.tsx
│   │   └── Footer.tsx
│   └── features/          # Feature-specific components
│       ├── auth/
│       │   └── AuthGuard.tsx
│       └── products/
│           ├── ProductCard.tsx
│           ├── ProductList.tsx
│           └── ProductSearch.tsx
├── lib/                   # Utilities
│   ├── api.ts            # API client
│   ├── auth.ts           # Auth utilities
│   ├── types.ts          # TypeScript types
│   └── utils.ts          # Helper functions
├── hooks/                 # Custom hooks
│   ├── useAuth.ts        # Authentication hook
│   ├── useApi.ts         # API hook
│   └── useProducts.ts    # Products hook
└── contexts/              # React contexts
    ├── AuthContext.tsx   # Auth state management
    └── ThemeContext.tsx  # Theme management
```

### Phase 3: Core Infrastructure (45-60 phút)

#### 3.1 TypeScript Types
```typescript
// lib/types.ts
export interface User {
  id: number
  username: string
  email: string
  full_name?: string
  is_active: boolean
  created_at: string
}

export interface Product {
  id: number
  name: string
  description?: string
  price: number
  quantity: number
  sku: string
  category?: string
  status: 'active' | 'inactive' | 'out_of_stock'
  is_featured: boolean
  owner_id: number
  created_at: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  username: string
  email: string
  password: string
  full_name?: string
}
```

#### 3.2 API Client
```typescript
// lib/api.ts
import axios from 'axios'
import { getCookie, setCookie, deleteCookie } from 'cookies-next'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor để thêm token
api.interceptors.request.use((config) => {
  const token = getCookie('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor để handle 401
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      deleteCookie('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)
```

#### 3.3 Authentication Context
```typescript
// contexts/AuthContext.tsx
'use client'
import { createContext, useContext, useEffect, useState } from 'react'
import { User } from '@/lib/types'
import { api } from '@/lib/api'

interface AuthContextType {
  user: User | null
  login: (username: string, password: string) => Promise<void>
  logout: () => void
  loading: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  // Implementation...
}
```

### Phase 4: Authentication Flow (60-90 phút)

#### 4.1 Login Page
- Form validation với react-hook-form + zod
- Error handling và loading states
- JWT token storage
- Redirect sau khi login thành công

#### 4.2 Register Page
- Username/email validation
- Password strength validation
- Success/error feedback

#### 4.3 Auth Guard
- Protected routes
- Automatic redirect
- Loading states

### Phase 5: Products Features (90-120 phút)

#### 5.1 Products List
- Pagination
- Search và filter
- Sort by price, name, date
- Product cards với image placeholder

#### 5.2 Product Detail
- Full product information
- Edit/Delete (nếu là owner)
- Stock management

#### 5.3 Create/Edit Product
- Form validation
- Image upload (optional)
- Categories selection
- Price formatting

### Phase 6: Dashboard & UX (45-60 phút)

#### 6.1 User Dashboard
- User profile
- User's products
- Statistics (total products, revenue, etc.)

#### 6.2 UI/UX Enhancements
- Loading skeletons
- Error boundaries
- Toast notifications
- Responsive design
- Dark/Light theme

### Phase 7: Advanced Features (Optional - 60-90 phút)

#### 7.1 Real-time Features
- WebSocket for notifications
- Real-time product updates

#### 7.2 Advanced Search
- Filter by multiple criteria
- Search suggestions
- Advanced pagination

#### 7.3 Performance Optimization
- Image optimization
- Code splitting
- Caching strategies

## 🚀 API Endpoints sẽ sử dụng

### Authentication
- `POST /auth/login` - Đăng nhập
- `POST /auth/register` - Đăng ký
- `GET /auth/me` - Lấy thông tin user
- `POST /auth/logout` - Đăng xuất

### Products
- `GET /products/` - Danh sách sản phẩm
- `POST /products/` - Tạo sản phẩm
- `GET /products/{id}` - Chi tiết sản phẩm
- `PUT /products/{id}` - Cập nhật sản phẩm
- `DELETE /products/{id}` - Xóa sản phẩm

### Users
- `GET /users/me` - Thông tin user hiện tại
- `PUT /users/me` - Cập nhật profile

## 📱 UI Components sẽ tạo

### Core UI
- Button (variants: primary, secondary, danger)
- Input (text, email, password, number)
- Card, Modal, Dropdown
- Loading spinner, Skeleton

### Feature Components
- ProductCard, ProductList, ProductSearch
- UserProfile, LoginForm, RegisterForm
- Header với navigation, Footer
- AuthGuard cho protected routes

## 🎨 Design System

### Colors
- Primary: Blue (#3B82F6)
- Secondary: Gray (#6B7280)
- Success: Green (#10B981)
- Warning: Yellow (#F59E0B)
- Error: Red (#EF4444)

### Typography
- Headings: font-bold
- Body: font-normal
- Small text: text-sm

### Spacing
- Consistent padding/margin scale
- Grid layout cho responsive

## 📊 State Management Strategy

1. **Local State**: useState cho component state
2. **Auth State**: React Context cho user authentication
3. **Server State**: Custom hooks với API calls
4. **Form State**: react-hook-form
5. **UI State**: useState cho modals, loading, etc.

## 🔒 Security Considerations

1. **JWT Storage**: httpOnly cookies vs localStorage
2. **Input Validation**: Client + server validation
3. **XSS Protection**: Sanitize user inputs
4. **CSRF Protection**: CSRF tokens
5. **Environment Variables**: Secure API keys

## 🧪 Testing Strategy (Optional)

1. **Unit Tests**: Jest + Testing Library
2. **Integration Tests**: API mocking
3. **E2E Tests**: Playwright/Cypress
4. **Type Safety**: TypeScript strict mode

Bạn muốn bắt đầu implement từ phase nào? Tôi khuyến nghị bắt đầu từ Phase 1-2 để setup project structure trước!
    