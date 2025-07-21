from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..core.database import get_database
from ..schemas.product import (
    ProductCreate, ProductUpdate, ProductResponse, 
    ProductSearch, StockUpdate, ProductListResponse
)
from ..schemas.user import UserResponse
from ..services.product_service import product_service
from .auth import get_current_active_user


# Tạo router với prefix và tags
router = APIRouter(prefix="/products", tags=["Products"])


class ProductRouter:
    """
    Class-based router cho Product management
    Thể hiện các nguyên lý OOP trong việc quản lý sản phẩm
    """
    
    def __init__(self):
        self.product_service = product_service
    
    def register_routes(self, router: APIRouter):
        """
        Đăng ký tất cả routes cho product management
        Thể hiện nguyên lý Encapsulation và Single Responsibility
        """
        # CRUD Operations
        router.add_api_route(
            "/",
            self.create_product,
            methods=["POST"],
            response_model=ProductResponse,
            status_code=status.HTTP_201_CREATED,
            summary="Tạo sản phẩm mới",
            description="Tạo sản phẩm mới với thông tin đầy đủ"
        )
        
        router.add_api_route(
            "/",
            self.get_products_list,
            methods=["GET"],
            response_model=ProductListResponse,
            summary="Lấy danh sách sản phẩm",
            description="Lấy danh sách sản phẩm với phân trang và tìm kiếm"
        )
        
        # Special Operations - PHẢI ĐẶT TRƯỚC {product_id}
        router.add_api_route(
            "/search",
            self.search_products,
            methods=["POST"],
            response_model=List[ProductResponse],
            summary="Tìm kiếm sản phẩm",
            description="Tìm kiếm sản phẩm theo nhiều tiêu chí"
        )
        
        router.add_api_route(
            "/featured",
            self.get_featured_products,
            methods=["GET"],
            response_model=List[ProductResponse],
            summary="Lấy sản phẩm nổi bật",
            description="Lấy danh sách sản phẩm được đánh dấu nổi bật"
        )
        
        router.add_api_route(
            "/category/{category}",
            self.get_products_by_category,
            methods=["GET"],
            response_model=List[ProductResponse],
            summary="Lấy sản phẩm theo danh mục",
            description="Lấy danh sách sản phẩm trong một danh mục"
        )
        
        router.add_api_route(
            "/my-products",
            self.get_my_products,
            methods=["GET"],
            response_model=List[ProductResponse],
            summary="Lấy sản phẩm của tôi",
            description="Lấy danh sách sản phẩm do user hiện tại sở hữu"
        )
        
        # Routes với path parameters - PHẢI ĐẶT SAU
        router.add_api_route(
            "/{product_id}",
            self.get_product_by_id,
            methods=["GET"],
            response_model=ProductResponse,
            summary="Lấy thông tin sản phẩm",
            description="Lấy thông tin chi tiết của một sản phẩm"
        )
        
        router.add_api_route(
            "/{product_id}",
            self.update_product,
            methods=["PUT"],
            response_model=ProductResponse,
            summary="Cập nhật sản phẩm",
            description="Cập nhật thông tin sản phẩm (chỉ owner)"
        )
        
        router.add_api_route(
            "/{product_id}",
            self.delete_product,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT,
            summary="Xóa sản phẩm",
            description="Xóa sản phẩm (chỉ owner)"
        )
        
        router.add_api_route(
            "/{product_id}/stock",
            self.update_stock,
            methods=["PATCH"],
            response_model=ProductResponse,
            summary="Cập nhật tồn kho",
            description="Cập nhật số lượng tồn kho sản phẩm"
        )
    
    async def create_product(
        self,
        product_data: ProductCreate,
        current_user: UserResponse = Depends(get_current_active_user),
        db: Session = Depends(get_database)
    ):
        """
        Tạo sản phẩm mới
        
        Args:
            product_data: Dữ liệu sản phẩm
            current_user: User hiện tại
            db: Database session
            
        Returns:
            ProductResponse: Sản phẩm đã tạo
        """
        try:
            product = self.product_service.create_product(
                db, product_data, current_user.id
            )
            return ProductResponse.from_orm(product)
        
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Lỗi server khi tạo sản phẩm"
            )
    
    async def get_products_list(
        self,
        skip: int = Query(0, ge=0, description="Số record bỏ qua"),
        limit: int = Query(100, ge=1, le=1000, description="Số record tối đa"),
        owner_id: Optional[int] = Query(None, description="Lọc theo owner ID"),
        db: Session = Depends(get_database)
    ):
        """
        Lấy danh sách sản phẩm với phân trang
        
        Args:
            skip: Số record bỏ qua
            limit: Số record tối đa
            owner_id: ID của owner (optional)
            db: Database session
            
        Returns:
            ProductListResponse: Danh sách sản phẩm với thông tin phân trang
        """
        products = self.product_service.get_products_list(
            db, skip=skip, limit=limit, owner_id=owner_id
        )
        total = self.product_service.get_product_count(db, owner_id=owner_id)
        
        return ProductListResponse(
            items=[ProductResponse.from_orm(product) for product in products],
            total=total,
            page=skip // limit + 1,
            size=limit,
            pages=(total + limit - 1) // limit
        )
    
    async def get_product_by_id(
        self,
        product_id: int,
        db: Session = Depends(get_database)
    ):
        """
        Lấy thông tin sản phẩm theo ID
        
        Args:
            product_id: ID của sản phẩm
            db: Database session
            
        Returns:
            ProductResponse: Thông tin sản phẩm
        """
        product = self.product_service.get_product_by_id(db, product_id)
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sản phẩm không tồn tại"
            )
        
        return ProductResponse.from_orm(product)
    
    async def update_product(
        self,
        product_id: int,
        product_data: ProductUpdate,
        current_user: UserResponse = Depends(get_current_active_user),
        db: Session = Depends(get_database)
    ):
        """
        Cập nhật sản phẩm
        
        Args:
            product_id: ID của sản phẩm
            product_data: Dữ liệu cập nhật
            current_user: User hiện tại
            db: Database session
            
        Returns:
            ProductResponse: Sản phẩm đã cập nhật
        """
        try:
            updated_product = self.product_service.update_product(
                db, product_id, product_data, current_user.id
            )
            
            if not updated_product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Sản phẩm không tồn tại"
                )
            
            return ProductResponse.from_orm(updated_product)
        
        except PermissionError as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Lỗi server khi cập nhật sản phẩm"
            )
    
    async def delete_product(
        self,
        product_id: int,
        current_user: UserResponse = Depends(get_current_active_user),
        db: Session = Depends(get_database)
    ):
        """
        Xóa sản phẩm
        
        Args:
            product_id: ID của sản phẩm
            current_user: User hiện tại
            db: Database session
        """
        try:
            success = self.product_service.delete_product(
                db, product_id, current_user.id
            )
            
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Sản phẩm không tồn tại"
                )
        
        except PermissionError as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Lỗi server khi xóa sản phẩm"
            )
    
    async def search_products(
        self,
        search_params: ProductSearch,
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        db: Session = Depends(get_database)
    ):
        """
        Tìm kiếm sản phẩm
        
        Args:
            search_params: Các tham số tìm kiếm
            skip: Số record bỏ qua
            limit: Số record tối đa
            db: Database session
            
        Returns:
            List[ProductResponse]: Danh sách sản phẩm tìm được
        """
        products = self.product_service.search_products(
            db, search_params, skip=skip, limit=limit
        )
        return [ProductResponse.from_orm(product) for product in products]
    
    async def update_stock(
        self,
        product_id: int,
        stock_update: StockUpdate,
        current_user: UserResponse = Depends(get_current_active_user),
        db: Session = Depends(get_database)
    ):
        """
        Cập nhật tồn kho sản phẩm
        
        Args:
            product_id: ID của sản phẩm
            stock_update: Thông tin cập nhật tồn kho
            current_user: User hiện tại
            db: Database session
            
        Returns:
            ProductResponse: Sản phẩm với tồn kho đã cập nhật
        """
        try:
            updated_product = self.product_service.update_stock(
                db, product_id, stock_update.quantity, current_user.id
            )
            
            if not updated_product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Sản phẩm không tồn tại"
                )
            
            return ProductResponse.from_orm(updated_product)
        
        except PermissionError as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e)
            )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Lỗi server khi cập nhật tồn kho"
            )
    
    async def get_featured_products(
        self,
        limit: int = Query(10, ge=1, le=100),
        db: Session = Depends(get_database)
    ):
        """
        Lấy sản phẩm nổi bật
        
        Args:
            limit: Số lượng sản phẩm tối đa
            db: Database session
            
        Returns:
            List[ProductResponse]: Danh sách sản phẩm nổi bật
        """
        products = self.product_service.get_featured_products(db, limit=limit)
        return [ProductResponse.from_orm(product) for product in products]
    
    async def get_products_by_category(
        self,
        category: str,
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        db: Session = Depends(get_database)
    ):
        """
        Lấy sản phẩm theo danh mục
        
        Args:
            category: Tên danh mục
            skip: Số record bỏ qua
            limit: Số record tối đa
            db: Database session
            
        Returns:
            List[ProductResponse]: Danh sách sản phẩm trong danh mục
        """
        products = self.product_service.get_products_by_category(
            db, category, skip=skip, limit=limit
        )
        return [ProductResponse.from_orm(product) for product in products]
    
    async def get_my_products(
        self,
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        current_user: UserResponse = Depends(get_current_active_user),
        db: Session = Depends(get_database)
    ):
        """
        Lấy danh sách sản phẩm của user hiện tại
        
        Args:
            skip: Số record bỏ qua
            limit: Số record tối đa
            current_user: User hiện tại
            db: Database session
            
        Returns:
            List[ProductResponse]: Danh sách sản phẩm của user
        """
        products = self.product_service.get_products_list(
            db, skip=skip, limit=limit, owner_id=current_user.id
        )
        return [ProductResponse.from_orm(product) for product in products]


# Khởi tạo product router instance và đăng ký routes
product_router = ProductRouter()
product_router.register_routes(router)
