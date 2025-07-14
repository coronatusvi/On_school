from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from ..core.security import security_manager
from ..core.exceptions import (
    ValidationException, ConflictException, ResourceNotFoundException,
    DatabaseException, error_handler
)


class BaseUserService(ABC):
    """
    Abstract base class cho User Service
    Thể hiện nguyên lý Abstraction trong OOP
    """
    
    @abstractmethod
    def create_user(self, db: Session, user_data: UserCreate) -> User:
        """Tạo user mới"""
        pass
    
    @abstractmethod
    def get_user_by_id(self, db: Session, user_id: int) -> Optional[User]:
        """Lấy user theo ID"""
        pass
    
    @abstractmethod
    def authenticate_user(self, db: Session, username: str, password: str) -> Optional[User]:
        """Xác thực user"""
        pass


class UserService(BaseUserService):
    """
    Service class cho User business logic
    Thể hiện các nguyên lý OOP:
    - Encapsulation: Ẩn chi tiết implementation
    - Inheritance: Kế thừa từ BaseUserService
    - Single Responsibility: Chỉ xử lý logic liên quan đến User
    """
    
    def __init__(self):
        """Constructor - khởi tạo dependencies"""
        self.security = security_manager
    
    def create_user(self, db: Session, user_data: UserCreate) -> User:
        """
        Tạo user mới với mã hóa mật khẩu
        
        Args:
            db: Database session
            user_data: Dữ liệu user từ request
            
        Returns:
            User: User object đã được tạo
            
        Raises:
            ConflictException: Nếu username hoặc email đã tồn tại
            ValidationException: Nếu dữ liệu không hợp lệ
            DatabaseException: Nếu có lỗi database
        """
        try:
            # Kiểm tra user đã tồn tại
            if self._user_exists(db, user_data.username, user_data.email):
                raise ConflictException("Username hoặc email đã tồn tại")
            
            # Hash password
            try:
                hashed_password = self.security.hash_password(user_data.password)
            except (ValueError, RuntimeError) as e:
                raise ValidationException(f"Lỗi mã hóa mật khẩu: {str(e)}")
            
            # Tạo user object
            user = User(
                username=user_data.username,
                email=user_data.email,
                hashed_password=hashed_password,
                full_name=user_data.full_name
            )
            
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
            
        except (ConflictException, ValidationException):
            db.rollback()
            raise
        except IntegrityError as e:
            db.rollback()
            raise error_handler.handle_database_error(e)
        except SQLAlchemyError as e:
            db.rollback()
            raise DatabaseException(f"Lỗi cơ sở dữ liệu: {str(e)}")
        except Exception as e:
            db.rollback()
            raise DatabaseException(f"Lỗi không xác định: {str(e)}")
    
    def get_user_by_id(self, db: Session, user_id: int) -> Optional[User]:
        """
        Lấy user theo ID
        
        Args:
            db: Database session
            user_id: ID của user
            
        Returns:
            Optional[User]: User object hoặc None
        """
        return db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_username(self, db: Session, username: str) -> Optional[User]:
        """
        Lấy user theo username
        
        Args:
            db: Database session
            username: Username của user
            
        Returns:
            Optional[User]: User object hoặc None
        """
        return db.query(User).filter(User.username == username).first()
    
    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        """
        Lấy user theo email
        
        Args:
            db: Database session
            email: Email của user
            
        Returns:
            Optional[User]: User object hoặc None
        """
        return db.query(User).filter(User.email == email).first()
    
    def authenticate_user(self, db: Session, username: str, password: str) -> Optional[User]:
        """
        Xác thực user với username/email và password
        
        Args:
            db: Database session
            username: Username hoặc email
            password: Password
            
        Returns:
            Optional[User]: User object nếu xác thực thành công, None nếu thất bại
        """
        # Tìm user theo username hoặc email
        user = self.get_user_by_username(db, username)
        if not user:
            user = self.get_user_by_email(db, username)
        
        if not user:
            return None
        
        # Kiểm tra password
        if not self.security.verify_password(password, user.hashed_password):
            return None
        
        # Kiểm tra user có active không
        if not user.is_active:
            return None
        
        return user
    
    def update_user(self, db: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """
        Cập nhật thông tin user
        
        Args:
            db: Database session
            user_id: ID của user
            user_data: Dữ liệu cập nhật
            
        Returns:
            Optional[User]: User object đã cập nhật hoặc None
        """
        user = self.get_user_by_id(db, user_id)
        if not user:
            return None
        
        # Cập nhật các fields
        update_data = user_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(user, field):
                setattr(user, field, value)
        
        try:
            db.commit()
            db.refresh(user)
            return user
        except IntegrityError:
            db.rollback()
            raise ValueError("Lỗi khi cập nhật user - email đã tồn tại")
    
    def delete_user(self, db: Session, user_id: int) -> bool:
        """
        Xóa user (soft delete bằng cách set is_active = False)
        
        Args:
            db: Database session
            user_id: ID của user
            
        Returns:
            bool: True nếu thành công, False nếu user không tồn tại
        """
        user = self.get_user_by_id(db, user_id)
        if not user:
            return False
        
        user.deactivate()
        db.commit()
        return True
    
    def get_users_list(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Lấy danh sách users với pagination
        
        Args:
            db: Database session
            skip: Số record bỏ qua
            limit: Số record tối đa
            
        Returns:
            List[User]: Danh sách users
        """
        return db.query(User).filter(User.is_active == True).offset(skip).limit(limit).all()
    
    def get_user_count(self, db: Session) -> int:
        """
        Đếm tổng số users active
        
        Args:
            db: Database session
            
        Returns:
            int: Số lượng users
        """
        return db.query(User).filter(User.is_active == True).count()
    
    def change_password(self, db: Session, user_id: int, new_password: str) -> bool:
        """
        Thay đổi mật khẩu user
        
        Args:
            db: Database session
            user_id: ID của user
            new_password: Mật khẩu mới
            
        Returns:
            bool: True nếu thành công
        """
        user = self.get_user_by_id(db, user_id)
        if not user:
            return False
        
        hashed_password = self.security.hash_password(new_password)
        user.hashed_password = hashed_password
        db.commit()
        return True
    
    def _user_exists(self, db: Session, username: str, email: str) -> bool:
        """
        Private method kiểm tra user đã tồn tại
        Thể hiện Encapsulation - ẩn implementation detail
        
        Args:
            db: Database session
            username: Username cần kiểm tra
            email: Email cần kiểm tra
            
        Returns:
            bool: True nếu user đã tồn tại
        """
        return db.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first() is not None


# Singleton instance
user_service = UserService()
