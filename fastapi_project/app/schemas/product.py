from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ProductStatus(str, Enum):
    """
    Enum cho trạng thái sản phẩm trong Pydantic
    """
    ACTIVE = "active"
    INACTIVE = "inactive"
    OUT_OF_STOCK = "out_of_stock"
    DISCONTINUED = "discontinued"


class ProductBase(BaseModel):
    """
    Base schema cho Product
    Áp dụng nguyên lý DRY và Encapsulation
    """
    name: str = Field(..., min_length=1, max_length=200, description="Tên sản phẩm")
    description: Optional[str] = Field(None, max_length=1000, description="Mô tả sản phẩm")
    price: float = Field(..., gt=0, description="Giá sản phẩm (phải > 0)")
    quantity: int = Field(default=0, ge=0, description="Số lượng tồn kho")
    sku: str = Field(..., min_length=1, max_length=50, description="Mã SKU")
    category: Optional[str] = Field(None, max_length=100, description="Danh mục")
    
    @validator('price')
    def validate_price(cls, v):
        """Validator cho giá - đảm bảo là số dương"""
        if v <= 0:
            raise ValueError('Giá sản phẩm phải lớn hơn 0')
        return round(v, 2)  # Làm tròn 2 chữ số thập phân
    
    @validator('sku')
    def validate_sku(cls, v):
        """Validator cho SKU - định dạng chuẩn"""
        if not v.replace('-', '').replace('_', '').isalnum():
            raise ValueError('SKU chỉ được chứa chữ, số, dấu gạch ngang và gạch dưới')
        return v.upper()


class ProductCreate(ProductBase):
    """
    Schema cho việc tạo sản phẩm mới
    Kế thừa từ ProductBase (Inheritance)
    """
    pass  # Không cần thêm field nào, sử dụng tất cả từ base


class ProductUpdate(BaseModel):
    """
    Schema cho việc cập nhật sản phẩm
    Tất cả fields đều optional
    """
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[float] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, ge=0)
    category: Optional[str] = Field(None, max_length=100)
    status: Optional[ProductStatus] = None
    is_featured: Optional[bool] = None
    
    @validator('price')
    def validate_price(cls, v):
        """Validator cho giá khi update"""
        if v is not None and v <= 0:
            raise ValueError('Giá sản phẩm phải lớn hơn 0')
        return round(v, 2) if v is not None else v


class ProductResponse(ProductBase):
    """
    Schema cho response trả về thông tin sản phẩm
    Kế thừa từ ProductBase và thêm các fields từ database
    """
    id: int
    status: ProductStatus
    is_featured: bool
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Computed fields
    is_available: bool = Field(..., description="Sản phẩm có sẵn để bán")
    total_value: float = Field(..., description="Tổng giá trị tồn kho")
    status_display: str = Field(..., description="Trạng thái dễ đọc")
    
    class Config:
        from_attributes = True  # Cho phép tạo từ ORM objects


class ProductInDB(ProductResponse):
    """
    Schema cho sản phẩm trong database
    Chứa đầy đủ thông tin, bao gồm cả owner information
    """
    pass


class ProductListResponse(BaseModel):
    """
    Schema cho danh sách sản phẩm với pagination
    """
    items: List[ProductResponse]
    total: int = Field(..., description="Tổng số sản phẩm")
    page: int = Field(..., description="Trang hiện tại")
    size: int = Field(..., description="Số item mỗi trang")
    pages: int = Field(..., description="Tổng số trang")


class ProductSearch(BaseModel):
    """
    Schema cho tìm kiếm sản phẩm
    """
    name: Optional[str] = Field(None, description="Tìm theo tên")
    category: Optional[str] = Field(None, description="Tìm theo danh mục") 
    min_price: Optional[float] = Field(None, ge=0, description="Giá tối thiểu")
    max_price: Optional[float] = Field(None, ge=0, description="Giá tối đa")
    status: Optional[ProductStatus] = Field(None, description="Trạng thái")
    is_featured: Optional[bool] = Field(None, description="Sản phẩm nổi bật")
    
    @validator('max_price')
    def validate_price_range(cls, v, values):
        """Validator để đảm bảo max_price >= min_price"""
        if v is not None and values.get('min_price') is not None:
            if v < values['min_price']:
                raise ValueError('Giá tối đa phải lớn hơn hoặc bằng giá tối thiểu')
        return v


class StockUpdate(BaseModel):
    """
    Schema cho cập nhật tồn kho
    """
    quantity: int = Field(..., description="Số lượng thay đổi (có thể âm để giảm)")
    reason: Optional[str] = Field(None, max_length=200, description="Lý do thay đổi")


# Aliases for API compatibility
ProductSearchRequest = ProductSearch
StockUpdateRequest = StockUpdate
