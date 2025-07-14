from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import List, Optional
from ..core.database import Base


class User(Base):
    """
    Model User sử dụng OOP principles
    - Encapsulation: Các thuộc tính private/protected
    - Inheritance: Kế thừa từ Base (SQLAlchemy)
    - Polymorphism: Override methods nếu cần
    """
    
    __tablename__ = "users"
    
    # Attributes (Encapsulation)
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    products = relationship("Product", back_populates="owner", cascade="all, delete-orphan")
    
    def __init__(self, username: str, email: str, hashed_password: str, 
                 full_name: Optional[str] = None, is_active: bool = True, 
                 is_superuser: bool = False):
        """
        Constructor với validation cơ bản
        """
        self.username = username
        self.email = email
        self.hashed_password = hashed_password
        self.full_name = full_name
        self.is_active = is_active
        self.is_superuser = is_superuser
    
    def __repr__(self) -> str:
        """String representation của object"""
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
    
    def __str__(self) -> str:
        """Human-readable string representation"""
        return f"User: {self.username} ({self.email})"
    
    # Business methods (Encapsulation của logic)
    def activate(self) -> None:
        """Kích hoạt user"""
        self.is_active = True
    
    def deactivate(self) -> None:
        """Vô hiệu hóa user"""
        self.is_active = False
    
    def make_superuser(self) -> None:
        """Biến user thành superuser"""
        self.is_superuser = True
    
    def remove_superuser(self) -> None:
        """Gỡ quyền superuser"""
        self.is_superuser = False
    
    def update_profile(self, full_name: Optional[str] = None, 
                      email: Optional[str] = None) -> None:
        """
        Cập nhật thông tin profile
        
        Args:
            full_name: Tên đầy đủ mới
            email: Email mới
        """
        if full_name is not None:
            self.full_name = full_name
        if email is not None:
            self.email = email
    
    @property
    def product_count(self) -> int:
        """Property để lấy số lượng sản phẩm của user"""
        return len(self.products) if self.products else 0
    
    @property
    def is_verified(self) -> bool:
        """Property kiểm tra user đã được xác thực chưa"""
        return self.is_active and not self.is_superuser
    
    def to_dict(self) -> dict:
        """
        Chuyển object thành dictionary (để serialize)
        Ẩn thông tin nhạy cảm như hashed_password
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "product_count": self.product_count
        }
