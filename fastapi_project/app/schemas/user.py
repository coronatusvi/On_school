from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    """
    Base schema cho User - áp dụng nguyên lý DRY (Don't Repeat Yourself)
    """
    username: str = Field(..., min_length=3, max_length=50, description="Tên đăng nhập")
    email: EmailStr = Field(..., description="Địa chỉ email")
    full_name: Optional[str] = Field(None, max_length=100, description="Họ và tên")
    
    @validator('username')
    def validate_username(cls, v):
        """Validator cho username"""
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username chỉ được chứa ký tự, số, dấu gạch ngang và gạch dưới')
        return v.lower()


class UserCreate(UserBase):
    """
    Schema cho việc tạo user mới
    Kế thừa từ UserBase (Inheritance)
    """
    password: str = Field(..., min_length=8, description="Mật khẩu (tối thiểu 8 ký tự)")
    
    @validator('password')
    def validate_password(cls, v):
        """Validator cho password - đảm bảo mật khẩu mạnh"""
        if len(v) < 8:
            raise ValueError('Mật khẩu phải có ít nhất 8 ký tự')
        if not any(c.isupper() for c in v):
            raise ValueError('Mật khẩu phải có ít nhất 1 chữ hoa')
        if not any(c.islower() for c in v):
            raise ValueError('Mật khẩu phải có ít nhất 1 chữ thường')
        if not any(c.isdigit() for c in v):
            raise ValueError('Mật khẩu phải có ít nhất 1 số')
        return v


class UserUpdate(BaseModel):
    """
    Schema cho việc cập nhật thông tin user
    Tất cả fields đều optional
    """
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    """
    Schema cho response trả về thông tin user
    Kế thừa từ UserBase và thêm các fields từ database
    """
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    product_count: int = Field(default=0, description="Số lượng sản phẩm")
    
    class Config:
        from_attributes = True  # Cho phép tạo từ ORM objects


class UserInDB(UserResponse):
    """
    Schema cho user trong database (bao gồm cả hashed_password)
    Chỉ sử dụng nội bộ, không expose ra API
    """
    hashed_password: str


class UserLogin(BaseModel):
    """
    Schema cho đăng nhập
    """
    username: str = Field(..., description="Tên đăng nhập hoặc email")
    password: str = Field(..., description="Mật khẩu")


class Token(BaseModel):
    """
    Schema cho JWT token response
    """
    access_token: str
    token_type: str = "bearer"
    expires_in: int = Field(..., description="Thời gian hết hạn (giây)")


class TokenData(BaseModel):
    """
    Schema cho dữ liệu trong JWT token
    """
    username: Optional[str] = None
    user_id: Optional[int] = None


class UserListResponse(BaseModel):
    """
    Schema cho response danh sách users với pagination
    """
    users: List[UserResponse]
    total: int = Field(..., description="Tổng số users")
    page: int = Field(..., description="Trang hiện tại")
    size: int = Field(..., description="Số lượng items per page")
    total_pages: int = Field(..., description="Tổng số trang")
    
    class Config:
        from_attributes = True
