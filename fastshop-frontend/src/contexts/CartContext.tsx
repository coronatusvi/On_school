'use client'

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react'
import { Cart, CartItem, Product } from '@/lib/types'
import toast from 'react-hot-toast'

interface CartContextType {
  cart: Cart
  loading: boolean
  addToCart: (product: Product, quantity?: number) => void
  removeFromCart: (itemId: string) => void
  updateQuantity: (itemId: string, quantity: number) => void
  clearCart: () => void
  getTotalItems: () => number
  getTotalAmount: () => number
  isInCart: (productId: number) => boolean
  getCartItem: (productId: number) => CartItem | undefined
}

const CartContext = createContext<CartContextType | undefined>(undefined)

interface CartProviderProps {
  children: ReactNode
}

const CART_STORAGE_KEY = 'fastshop_cart'

export function CartProvider({ children }: CartProviderProps) {
  const [cart, setCart] = useState<Cart>({
    items: [],
    total_items: 0,
    total_amount: 0,
  })
  const [loading, setLoading] = useState(true)

  // Load cart từ localStorage khi component mount
  useEffect(() => {
    loadCartFromStorage()
  }, [])

  // Save cart vào localStorage mỗi khi cart thay đổi
  useEffect(() => {
    if (!loading) {
      saveCartToStorage()
    }
  }, [cart, loading])

  const loadCartFromStorage = () => {
    try {
      if (typeof window !== 'undefined') {
        const savedCart = localStorage.getItem(CART_STORAGE_KEY)
        if (savedCart) {
          const parsedCart = JSON.parse(savedCart)
          setCart(parsedCart)
        }
      }
    } catch (error) {
      console.error('Error loading cart from storage:', error)
    } finally {
      setLoading(false)
    }
  }

  const saveCartToStorage = () => {
    try {
      if (typeof window !== 'undefined') {
        localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(cart))
      }
    } catch (error) {
      console.error('Error saving cart to storage:', error)
    }
  }

  const addToCart = (product: Product, quantity: number = 1) => {
    try {
      // Kiểm tra sản phẩm có sẵn không
      if (!product.is_available || product.quantity < 1) {
        toast.error('Sản phẩm hiện không có sẵn')
        return
      }

      setCart(prevCart => {
        const existingItemIndex = prevCart.items.findIndex(
          item => item.product.id === product.id
        )

        let newItems: CartItem[]

        if (existingItemIndex >= 0) {
          // Sản phẩm đã có trong giỏ hàng, update quantity
          const existingItem = prevCart.items[existingItemIndex]
          const newQuantity = existingItem.quantity + quantity

          // Kiểm tra không vượt quá tồn kho
          if (newQuantity > product.quantity) {
            toast.error(`Chỉ còn ${product.quantity} sản phẩm trong kho`)
            return prevCart
          }

          newItems = prevCart.items.map((item, index) => 
            index === existingItemIndex
              ? {
                  ...item,
                  quantity: newQuantity,
                  total: newQuantity * item.price
                }
              : item
          )
        } else {
          // Sản phẩm mới, thêm vào giỏ hàng
          if (quantity > product.quantity) {
            toast.error(`Chỉ còn ${product.quantity} sản phẩm trong kho`)
            return prevCart
          }

          const newItem: CartItem = {
            id: `${product.id}_${Date.now()}`,
            product,
            quantity,
            price: product.price,
            total: quantity * product.price
          }

          newItems = [...prevCart.items, newItem]
        }

        const totalItems = newItems.reduce((sum, item) => sum + item.quantity, 0)
        const totalAmount = newItems.reduce((sum, item) => sum + item.total, 0)

        toast.success('Đã thêm vào giỏ hàng!')

        return {
          items: newItems,
          total_items: totalItems,
          total_amount: totalAmount,
        }
      })
    } catch (error) {
      console.error('Error adding to cart:', error)
      toast.error('Có lỗi khi thêm sản phẩm vào giỏ hàng')
    }
  }

  const removeFromCart = (itemId: string) => {
    try {
      setCart(prevCart => {
        const newItems = prevCart.items.filter(item => item.id !== itemId)
        const totalItems = newItems.reduce((sum, item) => sum + item.quantity, 0)
        const totalAmount = newItems.reduce((sum, item) => sum + item.total, 0)

        toast.success('Đã xóa khỏi giỏ hàng!')

        return {
          items: newItems,
          total_items: totalItems,
          total_amount: totalAmount,
        }
      })
    } catch (error) {
      console.error('Error removing from cart:', error)
      toast.error('Có lỗi khi xóa sản phẩm khỏi giỏ hàng')
    }
  }

  const updateQuantity = (itemId: string, quantity: number) => {
    try {
      if (quantity < 1) {
        removeFromCart(itemId)
        return
      }

      setCart(prevCart => {
        const newItems = prevCart.items.map(item => {
          if (item.id === itemId) {
            // Kiểm tra không vượt quá tồn kho
            if (quantity > item.product.quantity) {
              toast.error(`Chỉ còn ${item.product.quantity} sản phẩm trong kho`)
              return item
            }

            return {
              ...item,
              quantity,
              total: quantity * item.price
            }
          }
          return item
        })

        const totalItems = newItems.reduce((sum, item) => sum + item.quantity, 0)
        const totalAmount = newItems.reduce((sum, item) => sum + item.total, 0)

        return {
          items: newItems,
          total_items: totalItems,
          total_amount: totalAmount,
        }
      })
    } catch (error) {
      console.error('Error updating quantity:', error)
      toast.error('Có lỗi khi cập nhật số lượng')
    }
  }

  const clearCart = () => {
    try {
      setCart({
        items: [],
        total_items: 0,
        total_amount: 0,
      })
      toast.success('Đã xóa toàn bộ giỏ hàng!')
    } catch (error) {
      console.error('Error clearing cart:', error)
      toast.error('Có lỗi khi xóa giỏ hàng')
    }
  }

  const getTotalItems = (): number => {
    return cart.total_items
  }

  const getTotalAmount = (): number => {
    return cart.total_amount
  }

  const isInCart = (productId: number): boolean => {
    return cart.items.some(item => item.product.id === productId)
  }

  const getCartItem = (productId: number): CartItem | undefined => {
    return cart.items.find(item => item.product.id === productId)
  }

  const contextValue: CartContextType = {
    cart,
    loading,
    addToCart,
    removeFromCart,
    updateQuantity,
    clearCart,
    getTotalItems,
    getTotalAmount,
    isInCart,
    getCartItem,
  }

  return (
    <CartContext.Provider value={contextValue}>
      {children}
    </CartContext.Provider>
  )
}

// Custom hook để sử dụng CartContext
export function useCart(): CartContextType {
  const context = useContext(CartContext)
  if (context === undefined) {
    throw new Error('useCart must be used within a CartProvider')
  }
  return context
}

export default CartProvider
