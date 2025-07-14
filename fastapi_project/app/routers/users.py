from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..core.database import get_database
from ..schemas.user import UserResponse, UserUpdate
from ..services.user_service import user_service
from .auth import get_current_active_user


# Tạo router với prefix và tags
router = APIRouter(prefix="/users", tags=["Users"])


class UserRouter:
    """
    Class-based router cho User management
    Thể hiện các nguyên lý OOP trong việc tổ chức API endpoints
    """
    
    def __init__(self):
        self.user_service = user_service
    
    def register_routes(self, router: APIRouter):
        """
        Đăng ký tất cả routes cho user management
        Thể hiện nguyên lý Encapsulation
        """
        router.add_api_route(
            "/me",
            self.get_current_user_profile,
            methods=["GET"],
            response_model=UserResponse,
            summary="Lấy thông tin profile hiện tại",
            description="Lấy thông tin chi tiết của user đang đăng nhập"
        )
        
        router.add_api_route(
            "/me",
            self.update_current_user_profile,
            methods=["PUT"],
            response_model=UserResponse,
            summary="Cập nhật profile hiện tại",
            description="Cập nhật thông tin profile của user đang đăng nhập"
        )
        
        router.add_api_route(
            "/",
            self.get_users_list,
            methods=["GET"],
            response_model=List[UserResponse],
            summary="Lấy danh sách users",
            description="Lấy danh sách tất cả users (có phân trang)"
        )
        
        router.add_api_route(
            "/{user_id}",
            self.get_user_by_id,
            methods=["GET"],
            response_model=UserResponse,
            summary="Lấy thông tin user theo ID",
            description="Lấy thông tin chi tiết của một user cụ thể"
        )
    
    async def get_current_user_profile(
        self,
        current_user: UserResponse = Depends(get_current_active_user)
    ):
        """
        Lấy thông tin profile của user hiện tại
        
        Args:
            current_user: User hiện tại từ JWT token
            
        Returns:
            UserResponse: Thông tin user hiện tại
        """
        return current_user
    
    async def update_current_user_profile(
        self,
        user_update: UserUpdate,
        current_user: UserResponse = Depends(get_current_active_user),
        db: Session = Depends(get_database)
    ):
        """
        Cập nhật thông tin profile của user hiện tại
        
        Args:
            user_update: Dữ liệu cập nhật
            current_user: User hiện tại từ JWT token
            db: Database session
            
        Returns:
            UserResponse: Thông tin user đã cập nhật
            
        Raises:
            HTTPException: Nếu có lỗi trong quá trình cập nhật
        """
        try:
            updated_user = self.user_service.update_user(
                db, current_user.id, user_update
            )
            
            if not updated_user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User không tồn tại"
                )
            
            return UserResponse.from_orm(updated_user)
        
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Lỗi server khi cập nhật user"
            )
    
    async def get_users_list(
        self,
        skip: int = Query(0, ge=0, description="Số record bỏ qua"),
        limit: int = Query(100, ge=1, le=1000, description="Số record tối đa"),
        current_user: UserResponse = Depends(get_current_active_user),
        db: Session = Depends(get_database)
    ):
        """
        Lấy danh sách users với phân trang
        
        Args:
            skip: Số record bỏ qua
            limit: Số record tối đa
            current_user: User hiện tại (để xác thực)
            db: Database session
            
        Returns:
            List[UserResponse]: Danh sách users
        """
        users = self.user_service.get_users_list(db, skip=skip, limit=limit)
        return [UserResponse.from_orm(user) for user in users]
    
    async def get_user_by_id(
        self,
        user_id: int,
        current_user: UserResponse = Depends(get_current_active_user),
        db: Session = Depends(get_database)
    ):
        """
        Lấy thông tin user theo ID
        
        Args:
            user_id: ID của user cần lấy
            current_user: User hiện tại (để xác thực)
            db: Database session
            
        Returns:
            UserResponse: Thông tin user
            
        Raises:
            HTTPException: Nếu user không tồn tại
        """
        user = self.user_service.get_user_by_id(db, user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User không tồn tại"
            )
        
        return UserResponse.from_orm(user)


# Khởi tạo user router instance và đăng ký routes
user_router = UserRouter()
user_router.register_routes(router)
