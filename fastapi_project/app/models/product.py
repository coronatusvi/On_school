from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum
from ..core.database import Base


class ProductStatus(Enum):
    """
    Enum cho trạng thái sản phẩm
    Sử dụng để thể hiện tính đa hình (Polymorphism)
    """
    ACTIVE = "active"
    INACTIVE = "inactive"
    OUT_OF_STOCK = "out_of_stock"
    DISCONTINUED = "discontinued"


class Product(Base):
    """
    Model Product thể hiện các nguyên lý OOP:
    - Encapsulation: Ẩn dữ liệu và cung cấp methods để truy cập
    - Inheritance: Kế thừa từ Base
    - Abstraction: Cung cấp interface rõ ràng cho business logic
    """
    
    __tablename__ = "products"
    
    # Attributes
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0)
    sku = Column(String(50), unique=True, index=True, nullable=False)
    category = Column(String(100), nullable=True)
    status = Column(String(20), default=ProductStatus.ACTIVE.value)
    is_featured = Column(Boolean, default=False)
    
    # Foreign Key
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship
    owner = relationship("User", back_populates="products")
    
    def __init__(self, name: str, price: float, sku: str, owner_id: int,
                 description: Optional[str] = None, quantity: int = 0, 
                 category: Optional[str] = None):
        """
        Constructor với validation
        """
        if price < 0:
            raise ValueError("Price cannot be negative")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
            
        self.name = name
        self.price = price
        self.sku = sku
        self.owner_id = owner_id
        self.description = description
        self.quantity = quantity
        self.category = category
        self.status = ProductStatus.ACTIVE.value
    
    def __repr__(self) -> str:
        """String representation cho debugging"""
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"
    
    def __str__(self) -> str:
        """Human-readable string representation"""
        return f"{self.name} - ${self.price} (SKU: {self.sku})"
    
    # Business Methods (Encapsulation)
    def update_price(self, new_price: float) -> None:
        """
        Cập nhật giá sản phẩm với validation
        
        Args:
            new_price: Giá mới
            
        Raises:
            ValueError: Nếu giá âm
        """
        if new_price < 0:
            raise ValueError("Price cannot be negative")
        self.price = new_price
    
    def add_stock(self, quantity: int) -> None:
        """
        Thêm số lượng tồn kho
        
        Args:
            quantity: Số lượng cần thêm
        """
        if quantity < 0:
            raise ValueError("Quantity to add cannot be negative")
        self.quantity += quantity
        
        # Tự động active nếu có hàng
        if self.quantity > 0 and self.status == ProductStatus.OUT_OF_STOCK.value:
            self.status = ProductStatus.ACTIVE.value
    
    def remove_stock(self, quantity: int) -> bool:
        """
        Giảm số lượng tồn kho
        
        Args:
            quantity: Số lượng cần giảm
            
        Returns:
            bool: True nếu thành công, False nếu không đủ hàng
        """
        if quantity < 0:
            raise ValueError("Quantity to remove cannot be negative")
        
        if self.quantity < quantity:
            return False
        
        self.quantity -= quantity
        
        # Tự động chuyển sang out of stock nếu hết hàng
        if self.quantity == 0:
            self.status = ProductStatus.OUT_OF_STOCK.value
            
        return True
    
    def activate(self) -> None:
        """Kích hoạt sản phẩm"""
        if self.quantity > 0:
            self.status = ProductStatus.ACTIVE.value
        else:
            self.status = ProductStatus.OUT_OF_STOCK.value
    
    def deactivate(self) -> None:
        """Vô hiệu hóa sản phẩm"""
        self.status = ProductStatus.INACTIVE.value
    
    def discontinue(self) -> None:
        """Ngừng bán sản phẩm"""
        self.status = ProductStatus.DISCONTINUED.value
    
    def make_featured(self) -> None:
        """Đánh dấu là sản phẩm nổi bật"""
        self.is_featured = True
    
    def remove_featured(self) -> None:
        """Gỡ đánh dấu sản phẩm nổi bật"""
        self.is_featured = False
    
    # Properties (Getter methods)
    @property
    def is_available(self) -> bool:
        """Kiểm tra sản phẩm có sẵn để bán không"""
        return (self.status == ProductStatus.ACTIVE.value and 
                self.quantity > 0)
    
    @property
    def total_value(self) -> float:
        """Tính tổng giá trị tồn kho"""
        return self.price * self.quantity
    
    @property
    def status_display(self) -> str:
        """Hiển thị trạng thái dễ đọc"""
        status_map = {
            ProductStatus.ACTIVE.value: "Đang bán",
            ProductStatus.INACTIVE.value: "Tạm ngừng",
            ProductStatus.OUT_OF_STOCK.value: "Hết hàng",
            ProductStatus.DISCONTINUED.value: "Ngừng sản xuất"
        }
        return status_map.get(self.status, "Không xác định")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Chuyển object thành dictionary
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "quantity": self.quantity,
            "sku": self.sku,
            "category": self.category,
            "status": self.status,
            "status_display": self.status_display,
            "is_featured": self.is_featured,
            "is_available": self.is_available,
            "total_value": self.total_value,
            "owner_id": self.owner_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
