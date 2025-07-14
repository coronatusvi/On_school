from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Optional

from ..core.database import get_database
from ..core.security import security_manager
from ..core.exceptions import (
    ValidationException, AuthenticationException, ConflictException,
    ResourceNotFoundException, error_handler
)
from ..schemas.user import UserCreate, UserLogin, Token, UserResponse
from ..services.user_service import user_service


# Tạo router với prefix và tags
router = APIRouter(prefix="/auth", tags=["Authentication"])

# Security scheme
security = HTTPBearer()


class AuthenticationRouter:
    """
    Class-based router cho Authentication
    Thể hiện nguyên lý OOP trong việc tổ chức router
    """
    
    def __init__(self):
        self.user_service = user_service
        self.security_manager = security_manager
    
    def register_routes(self, router: APIRouter):
        """
        Đăng ký tất cả routes cho router
        Thể hiện nguyên lý Encapsulation
        """
        router.add_api_route(
            "/register",
            self.register,
            methods=["POST"],
            response_model=UserResponse,
            status_code=status.HTTP_201_CREATED,
            summary="Đăng ký user mới",
            description="Tạo tài khoản user mới với username, email và password"
        )
        
        router.add_api_route(
            "/login",
            self.login,
            methods=["POST"],
            response_model=Token,
            summary="Đăng nhập",
            description="Đăng nhập với username/email và password để nhận JWT token"
        )
    
    async def register(self, user_data: UserCreate, db: Session = Depends(get_database)):
        """
        Endpoint đăng ký user mới
        
        Args:
            user_data: Thông tin user cần tạo
            db: Database session
            
        Returns:
            UserResponse: Thông tin user đã tạo
            
        Raises:
            HTTPException: Nếu có lỗi trong quá trình tạo user
        """
        try:
            user = self.user_service.create_user(db, user_data)
            return UserResponse.from_orm(user)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Lỗi server khi tạo user"
            )
    
    async def login(self, login_data: UserLogin, db: Session = Depends(get_database)):
        """
        Endpoint đăng nhập
        
        Args:
            login_data: Thông tin đăng nhập
            db: Database session
            
        Returns:
            Token: JWT access token
            
        Raises:
            HTTPException: Nếu thông tin đăng nhập không đúng
        """
        # Xác thực user
        user = self.user_service.authenticate_user(
            db, login_data.username, login_data.password
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Username/email hoặc password không đúng",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Tạo access token
        access_token_expires = timedelta(minutes=self.security_manager.access_token_expire_minutes)
        access_token = self.security_manager.create_access_token(
            data={"sub": user.username, "user_id": user.id},
            expires_delta=access_token_expires
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=self.security_manager.access_token_expire_minutes * 60
        )


# Dependency để lấy current user từ JWT token
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_database)
) -> Optional[UserResponse]:
    """
    Dependency function để lấy thông tin user hiện tại từ JWT token
    
    Args:
        credentials: JWT token từ Authorization header
        db: Database session
        
    Returns:
        UserResponse: Thông tin user hiện tại
        
    Raises:
        HTTPException: Nếu token không hợp lệ hoặc user không tồn tại
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    try:
        # Verify JWT token
        payload = security_manager.verify_token(credentials.credentials)
        if payload is None:
            raise credentials_exception
        
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        
        if username is None or user_id is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    
    # Lấy user từ database
    user = user_service.get_user_by_id(db, user_id)
    if user is None:
        raise credentials_exception
    
    return UserResponse.from_orm(user)


# Dependency để kiểm tra user active
async def get_current_active_user(
    current_user: UserResponse = Depends(get_current_user)
) -> UserResponse:
    """
    Dependency function để đảm bảo user hiện tại đang active
    
    Args:
        current_user: User hiện tại từ get_current_user
        
    Returns:
        UserResponse: User active
        
    Raises:
        HTTPException: Nếu user không active
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


# Khởi tạo auth router instance và đăng ký routes
auth_router = AuthenticationRouter()
auth_router.register_routes(router)
