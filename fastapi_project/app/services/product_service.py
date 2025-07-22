from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..models.product import Product
from ..schemas.product import ProductCreate, ProductUpdate, ProductSearchRequest
from ..crud.product import product_repository
from ..crud.user import user_repository
from ..core.exceptions import (
    ValidationException, ConflictException, ResourceNotFoundException,
    DatabaseException, UnauthorizedException
)


class BaseProductService(ABC):
    """
    Abstract base class for Product Service
    Implements the Interface Segregation Principle (SOLID)
    """
    
    @abstractmethod
    def create_product(self, db: Session, *, product_data: ProductCreate, owner_id: int) -> Product:
        """Create a new product"""
        pass
    
    @abstractmethod
    def get_product_by_id(self, db: Session, *, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        pass
    
    @abstractmethod
    def update_product(self, db: Session, *, product: Product, product_update: ProductUpdate) -> Product:
        """Update product"""
        pass


class ProductService(BaseProductService):
    """
    Product Service implementing business logic using Repository Pattern
    
    This class follows SOLID principles:
    - Single Responsibility: Handles product business logic only
    - Open/Closed: Can be extended without modification
    - Liskov Substitution: Can replace BaseProductService
    - Interface Segregation: Specific interfaces for specific operations
    - Dependency Inversion: Depends on Repository abstraction
    """
    
    def __init__(self):
        """Initialize service with dependencies"""
        self.product_repo = product_repository
        self.user_repo = user_repository
    
    def create_product(self, db: Session, *, product_data: ProductCreate, owner_id: int) -> Product:
        """
        Create a new product with business logic validation
        
        Args:
            db: Database session
            product_data: Product creation data
            owner_id: ID of the product owner
            
        Returns:
            Created product instance
            
        Raises:
            ResourceNotFoundException: If owner not found
            ValidationException: If validation fails
            DatabaseException: If database operation fails
        """
        try:
            # Verify owner exists
            owner = self.user_repo.get(db, id=owner_id)
            if not owner:
                raise ResourceNotFoundException(f"Owner with ID {owner_id} not found")
            
            # Create product data with owner_id
            product_dict = product_data.dict()
            product_dict["owner_id"] = owner_id
            
            # Create product through repository
            product = self.product_repo.create(db, obj_in=product_dict)
            
            return product
            
        except IntegrityError as e:
            raise ConflictException("Product creation failed due to constraint violation")
        except Exception as e:
            raise DatabaseException(f"Failed to create product: {str(e)}")
    
    def get_product_by_id(self, db: Session, *, product_id: int) -> Optional[Product]:
        """
        Get product by ID with error handling
        
        Args:
            db: Database session
            product_id: Product ID to search for
            
        Returns:
            Product instance or None if not found
        """
        try:
            return self.product_repo.get(db, id=product_id)
        except Exception as e:
            raise DatabaseException(f"Failed to get product: {str(e)}")
    
    def get_product_by_id_or_404(self, db: Session, *, product_id: int) -> Product:
        """
        Get product by ID or raise 404 exception
        
        Args:
            db: Database session
            product_id: Product ID to search for
            
        Returns:
            Product instance
            
        Raises:
            ResourceNotFoundException: If product not found
        """
        product = self.get_product_by_id(db, product_id=product_id)
        if not product:
            raise ResourceNotFoundException(f"Product with ID {product_id} not found")
        return product
    
    def update_product(self, db: Session, *, product: Product, product_update: ProductUpdate, user_id: int) -> Product:
        """
        Update product with ownership validation
        
        Args:
            db: Database session
            product: Product instance to update
            product_update: Update data
            user_id: ID of the user requesting the update
            
        Returns:
            Updated product instance
            
        Raises:
            UnauthorizedException: If user is not the owner
            ValidationException: If validation fails
        """
        try:
            # Check ownership
            if product.owner_id != user_id:
                raise UnauthorizedException("You can only update your own products")
            
            # Update product through repository
            return self.product_repo.update(db, db_obj=product, obj_in=product_update)
            
        except Exception as e:
            raise DatabaseException(f"Failed to update product: {str(e)}")
    
    def delete_product(self, db: Session, *, product_id: int, user_id: int) -> bool:
        """
        Delete product with ownership validation
        
        Args:
            db: Database session
            product_id: Product ID to delete
            user_id: ID of the user requesting the deletion
            
        Returns:
            True if deletion successful
            
        Raises:
            ResourceNotFoundException: If product not found
            UnauthorizedException: If user is not the owner
        """
        try:
            product = self.get_product_by_id_or_404(db, product_id=product_id)
            
            # Check ownership
            if product.owner_id != user_id:
                raise UnauthorizedException("You can only delete your own products")
            
            deleted_product = self.product_repo.delete(db, id=product_id)
            return deleted_product is not None
            
        except Exception as e:
            raise DatabaseException(f"Failed to delete product: {str(e)}")
    
    def get_products_list(
        self, 
        db: Session, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        search: Optional[str] = None,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        in_stock: Optional[bool] = None,
        is_featured: Optional[bool] = None
    ) -> List[Product]:
        """
        Get list of products with filtering
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            search: Search query for product name or description
            category: Filter by category
            min_price: Minimum price filter
            max_price: Maximum price filter
            in_stock: Filter by stock availability
            is_featured: Filter by featured status
            
        Returns:
            List of product instances
        """
        try:
            if search:
                return self.product_repo.search_products(db, search_query=search, skip=skip, limit=limit)
            
            return self.product_repo.advanced_search(
                db,
                category=category,
                min_price=min_price,
                max_price=max_price,
                in_stock=in_stock,
                is_featured=is_featured,
                skip=skip,
                limit=limit
            )
            
        except Exception as e:
            raise DatabaseException(f"Failed to get products list: {str(e)}")
    
    def get_featured_products(self, db: Session, *, limit: int = 10) -> List[Product]:
        """
        Get featured products
        
        Args:
            db: Database session
            limit: Maximum number of products to return
            
        Returns:
            List of featured product instances
        """
        try:
            return self.product_repo.get_featured_products(db, limit=limit)
        except Exception as e:
            raise DatabaseException(f"Failed to get featured products: {str(e)}")
    
    def get_products_by_category(self, db: Session, *, category: str, skip: int = 0, limit: int = 100) -> List[Product]:
        """
        Get products by category
        
        Args:
            db: Database session
            category: Product category
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of product instances
        """
        try:
            return self.product_repo.get_by_category(db, category=category, skip=skip, limit=limit)
        except Exception as e:
            raise DatabaseException(f"Failed to get products by category: {str(e)}")
    
    def get_my_products(self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100) -> List[Product]:
        """
        Get products owned by a specific user
        
        Args:
            db: Database session
            owner_id: ID of the product owner
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of product instances
        """
        try:
            return self.product_repo.get_by_owner(db, owner_id=owner_id, skip=skip, limit=limit)
        except Exception as e:
            raise DatabaseException(f"Failed to get user products: {str(e)}")
    
    def search_products(self, db: Session, *, search_request: ProductSearchRequest) -> List[Product]:
        """
        Advanced product search
        
        Args:
            db: Database session
            search_request: Search criteria
            
        Returns:
            List of matching product instances
        """
        try:
            return self.product_repo.advanced_search(
                db,
                name=search_request.name,
                category=search_request.category,
                min_price=search_request.min_price,
                max_price=search_request.max_price,
                in_stock=search_request.in_stock,
                is_featured=search_request.is_featured,
                skip=search_request.skip or 0,
                limit=search_request.limit or 100
            )
        except Exception as e:
            raise DatabaseException(f"Failed to search products: {str(e)}")
    
    def update_stock(self, db: Session, *, product_id: int, new_stock: int, user_id: int) -> Product:
        """
        Update product stock with ownership validation
        
        Args:
            db: Database session
            product_id: Product ID to update
            new_stock: New stock quantity
            user_id: ID of the user requesting the update
            
        Returns:
            Updated product instance
            
        Raises:
            ResourceNotFoundException: If product not found
            UnauthorizedException: If user is not the owner
            ValidationException: If stock value is invalid
        """
        try:
            product = self.get_product_by_id_or_404(db, product_id=product_id)
            
            # Check ownership
            if product.owner_id != user_id:
                raise UnauthorizedException("You can only update stock for your own products")
            
            # Validate stock value
            if new_stock < 0:
                raise ValidationException("Stock quantity cannot be negative")
            
            return self.product_repo.update_stock(db, product=product, new_stock=new_stock)
            
        except Exception as e:
            raise DatabaseException(f"Failed to update product stock: {str(e)}")
    
    def set_featured_status(self, db: Session, *, product_id: int, is_featured: bool, user_id: int) -> Product:
        """
        Set product featured status with ownership validation
        
        Args:
            db: Database session
            product_id: Product ID to update
            is_featured: Whether to feature the product
            user_id: ID of the user requesting the update
            
        Returns:
            Updated product instance
            
        Raises:
            ResourceNotFoundException: If product not found
            UnauthorizedException: If user is not the owner
        """
        try:
            product = self.get_product_by_id_or_404(db, product_id=product_id)
            
            # Check ownership
            if product.owner_id != user_id:
                raise UnauthorizedException("You can only update featured status for your own products")
            
            return self.product_repo.set_featured(db, product=product, is_featured=is_featured)
            
        except Exception as e:
            raise DatabaseException(f"Failed to update featured status: {str(e)}")
    
    def get_popular_categories(self, db: Session, *, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get popular product categories
        
        Args:
            db: Database session
            limit: Maximum number of categories to return
            
        Returns:
            List of categories with product counts
        """
        try:
            return self.product_repo.get_popular_categories(db, limit=limit)
        except Exception as e:
            raise DatabaseException(f"Failed to get popular categories: {str(e)}")
    
    def get_low_stock_products(self, db: Session, *, threshold: int = 10, owner_id: Optional[int] = None) -> List[Product]:
        """
        Get products with low stock
        
        Args:
            db: Database session
            threshold: Stock quantity threshold
            owner_id: Optional owner ID to filter by
            
        Returns:
            List of products with low stock
        """
        try:
            if owner_id:
                # Get low stock products for specific owner
                products = self.product_repo.get_by_owner(db, owner_id=owner_id, skip=0, limit=1000)
                return [p for p in products if p.stock_quantity <= threshold]
            else:
                return self.product_repo.get_low_stock_products(db, threshold=threshold)
        except Exception as e:
            raise DatabaseException(f"Failed to get low stock products: {str(e)}")
    
    def get_product_stats(self, db: Session, *, owner_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Get product statistics
        
        Args:
            db: Database session
            owner_id: Optional owner ID to filter by
            
        Returns:
            Dictionary with product statistics
        """
        try:
            if owner_id:
                # Stats for specific owner
                filters = {"owner_id": owner_id, "is_active": True}
                total_products = self.product_repo.count(db, filters=filters)
                
                filters["is_featured"] = True
                featured_products = self.product_repo.count(db, filters=filters)
                
                # Get low stock count
                products = self.product_repo.get_by_owner(db, owner_id=owner_id, skip=0, limit=1000)
                low_stock_products = len([p for p in products if p.stock_quantity <= 10])
                
                return {
                    "total_products": total_products,
                    "featured_products": featured_products,
                    "low_stock_products": low_stock_products
                }
            else:
                # Global stats
                total_products = self.product_repo.count(db, filters={"is_active": True})
                featured_products = self.product_repo.count(db, filters={"is_active": True, "is_featured": True})
                low_stock_products = len(self.product_repo.get_low_stock_products(db, threshold=10, skip=0, limit=1000))
                
                return {
                    "total_products": total_products,
                    "featured_products": featured_products,
                    "low_stock_products": low_stock_products
                }
                
        except Exception as e:
            raise DatabaseException(f"Failed to get product stats: {str(e)}")


# Create a singleton instance
product_service = ProductService()
