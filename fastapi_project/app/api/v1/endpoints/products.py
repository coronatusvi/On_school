from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Any, Dict

from ....core.database import get_database
from ....core.security import get_current_active_user
from ....models.user import User
from ....schemas.product import (
    ProductCreate, ProductResponse, ProductUpdate, ProductListResponse,
    ProductSearchRequest, StockUpdateRequest
)
from ....services.product_service import product_service
from ....core.exceptions import (
    ValidationException, ConflictException, ResourceNotFoundException,
    DatabaseException, UnauthorizedException
)

router = APIRouter()


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
) -> Any:
    """
    Create a new product
    
    - **name**: Product name (required)
    - **description**: Product description
    - **price**: Product price (must be positive)
    - **category**: Product category
    - **stock_quantity**: Initial stock quantity
    - **is_featured**: Whether to feature the product
    """
    try:
        product = product_service.create_product(
            db, 
            product_data=product_data, 
            owner_id=current_user.id
        )
        return ProductResponse.from_orm(product)
        
    except ConflictException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except DatabaseException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/", response_model=ProductListResponse)
async def get_products_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    in_stock: Optional[bool] = Query(None),
    is_featured: Optional[bool] = Query(None),
    db: Session = Depends(get_database)
) -> Any:
    """
    Get list of products with optional filtering
    
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    - **search**: Search in product name or description
    - **category**: Filter by category
    - **min_price**: Minimum price filter
    - **max_price**: Maximum price filter
    - **in_stock**: Filter by stock availability
    - **is_featured**: Filter by featured status
    """
    try:
        products = product_service.get_products_list(
            db,
            skip=skip,
            limit=limit,
            search=search,
            category=category,
            min_price=min_price,
            max_price=max_price,
            in_stock=in_stock,
            is_featured=is_featured
        )
        
        total = product_service.product_repo.count(db, filters={"is_active": True})
        
        return ProductListResponse(
            products=[ProductResponse.from_orm(product) for product in products],
            total=total,
            skip=skip,
            limit=limit
        )
        
    except DatabaseException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/featured", response_model=List[ProductResponse])
async def get_featured_products(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_database)
) -> Any:
    """
    Get featured products
    
    - **limit**: Maximum number of featured products to return
    """
    try:
        products = product_service.get_featured_products(db, limit=limit)
        return [ProductResponse.from_orm(product) for product in products]
        
    except DatabaseException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/category/{category}", response_model=List[ProductResponse])
async def get_products_by_category(
    category: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_database)
) -> Any:
    """
    Get products by category
    
    - **category**: Product category
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    """
    try:
        products = product_service.get_products_by_category(
            db, 
            category=category, 
            skip=skip, 
            limit=limit
        )
        return [ProductResponse.from_orm(product) for product in products]
        
    except DatabaseException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/my-products", response_model=List[ProductResponse])
async def get_my_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
) -> Any:
    """
    Get products owned by current user
    
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    """
    try:
        products = product_service.get_my_products(
            db, 
            owner_id=current_user.id, 
            skip=skip, 
            limit=limit
        )
        return [ProductResponse.from_orm(product) for product in products]
        
    except DatabaseException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/search", response_model=List[ProductResponse])
async def search_products(
    search_request: ProductSearchRequest,
    db: Session = Depends(get_database)
) -> Any:
    """
    Advanced product search
    
    Search products with multiple criteria:
    - **name**: Product name to search for
    - **category**: Product category
    - **min_price**: Minimum price
    - **max_price**: Maximum price
    - **in_stock**: Stock availability
    - **is_featured**: Featured status
    - **skip**: Pagination offset
    - **limit**: Maximum results
    """
    try:
        products = product_service.search_products(db, search_request=search_request)
        return [ProductResponse.from_orm(product) for product in products]
        
    except DatabaseException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product_by_id(
    product_id: int,
    db: Session = Depends(get_database)
) -> Any:
    """
    Get product by ID
    
    - **product_id**: Product ID
    """
    try:
        product = product_service.get_product_by_id_or_404(db, product_id=product_id)
        return ProductResponse.from_orm(product)
        
    except ResourceNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except DatabaseException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
) -> Any:
    """
    Update product
    
    Only the product owner can update their products
    
    - **name**: Updated product name
    - **description**: Updated description
    - **price**: Updated price
    - **category**: Updated category
    - **is_featured**: Updated featured status
    """
    try:
        product = product_service.get_product_by_id_or_404(db, product_id=product_id)
        updated_product = product_service.update_product(
            db, 
            product=product, 
            product_update=product_update, 
            user_id=current_user.id
        )
        return ProductResponse.from_orm(updated_product)
        
    except ResourceNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except UnauthorizedException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except DatabaseException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
):
    """
    Delete product
    
    Only the product owner can delete their products
    
    - **product_id**: Product ID to delete
    """
    try:
        success = product_service.delete_product(
            db, 
            product_id=product_id, 
            user_id=current_user.id
        )
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete product"
            )
        return None
        
    except ResourceNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except UnauthorizedException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except DatabaseException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.patch("/{product_id}/stock", response_model=ProductResponse)
async def update_product_stock(
    product_id: int,
    stock_update: StockUpdateRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
) -> Any:
    """
    Update product stock quantity
    
    Only the product owner can update stock
    
    - **stock_quantity**: New stock quantity
    """
    try:
        updated_product = product_service.update_stock(
            db, 
            product_id=product_id, 
            new_stock=stock_update.stock_quantity, 
            user_id=current_user.id
        )
        return ProductResponse.from_orm(updated_product)
        
    except ResourceNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except UnauthorizedException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except DatabaseException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.patch("/{product_id}/featured", response_model=ProductResponse)
async def set_product_featured(
    product_id: int,
    is_featured: bool,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
) -> Any:
    """
    Set product featured status
    
    Only the product owner can change featured status
    
    - **is_featured**: Whether to feature the product
    """
    try:
        updated_product = product_service.set_featured_status(
            db, 
            product_id=product_id, 
            is_featured=is_featured, 
            user_id=current_user.id
        )
        return ProductResponse.from_orm(updated_product)
        
    except ResourceNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except UnauthorizedException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except DatabaseException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/stats/categories", response_model=List[Dict[str, Any]])
async def get_popular_categories(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_database)
) -> Any:
    """
    Get popular product categories
    
    - **limit**: Maximum number of categories to return
    """
    try:
        categories = product_service.get_popular_categories(db, limit=limit)
        return categories
        
    except DatabaseException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/stats/overview")
async def get_product_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
) -> Dict[str, Any]:
    """
    Get product statistics overview for current user
    """
    try:
        stats = product_service.get_product_stats(db, owner_id=current_user.id)
        return stats
        
    except DatabaseException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/stats/low-stock", response_model=List[ProductResponse])
async def get_low_stock_products(
    threshold: int = Query(10, ge=0),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_database)
) -> Any:
    """
    Get products with low stock for current user
    
    - **threshold**: Stock quantity threshold
    """
    try:
        products = product_service.get_low_stock_products(
            db, 
            threshold=threshold, 
            owner_id=current_user.id
        )
        return [ProductResponse.from_orm(product) for product in products]
        
    except DatabaseException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
