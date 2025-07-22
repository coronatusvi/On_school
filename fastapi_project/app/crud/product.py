from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc

from .base import BaseRepository
from ..models.product import Product, ProductStatus
from ..schemas.product import ProductCreate, ProductUpdate


class ProductRepository(BaseRepository[Product, ProductCreate, ProductUpdate]):
    """
    Product Repository implementing specific product operations
    
    Inherits from BaseRepository and adds product-specific methods
    following the Repository Pattern and SOLID principles
    """

    def __init__(self):
        super().__init__(Product)

    def get_by_field(self, db: Session, *, field: str, value: Any) -> Optional[Product]:
        """
        Get product by any field (implementation of abstract method)
        
        Args:
            db: Database session
            field: Field name to search by
            value: Value to search for
            
        Returns:
            Product instance or None if not found
        """
        if hasattr(Product, field):
            return db.query(Product).filter(getattr(Product, field) == value).first()
        return None

    def get_by_owner(self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100) -> List[Product]:
        """
        Get products by owner ID
        
        Args:
            db: Database session
            owner_id: ID of the product owner
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of product instances
        """
        return db.query(Product).filter(Product.owner_id == owner_id).offset(skip).limit(limit).all()

    def get_active_products(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Product]:
        """
        Get all active products
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of active product instances
        """
        return db.query(Product).filter(
            Product.is_active == True,
            Product.stock_quantity > 0
        ).offset(skip).limit(limit).all()

    def get_featured_products(self, db: Session, *, limit: int = 10) -> List[Product]:
        """
        Get featured products
        
        Args:
            db: Database session
            limit: Maximum number of products to return
            
        Returns:
            List of featured product instances
        """
        return db.query(Product).filter(
            Product.is_featured == True,
            Product.is_active == True,
            Product.stock_quantity > 0
        ).order_by(desc(Product.created_at)).limit(limit).all()

    def get_by_category(self, db: Session, *, category: str, skip: int = 0, limit: int = 100) -> List[Product]:
        """
        Get products by category
        
        Args:
            db: Database session
            category: Product category
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of product instances in the category
        """
        return db.query(Product).filter(
            Product.category == category,
            Product.is_active == True
        ).offset(skip).limit(limit).all()

    def search_products(self, db: Session, *, search_query: str, skip: int = 0, limit: int = 100) -> List[Product]:
        """
        Search products by name, description, or category
        
        Args:
            db: Database session
            search_query: Search query string
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of matching product instances
        """
        search_filter = or_(
            Product.name.contains(search_query),
            Product.description.contains(search_query),
            Product.category.contains(search_query)
        )
        
        return db.query(Product).filter(
            search_filter,
            Product.is_active == True
        ).offset(skip).limit(limit).all()

    def get_by_price_range(
        self, 
        db: Session, 
        *, 
        min_price: Optional[float] = None, 
        max_price: Optional[float] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Product]:
        """
        Get products within a price range
        
        Args:
            db: Database session
            min_price: Minimum price (optional)
            max_price: Maximum price (optional)
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of product instances within the price range
        """
        query = db.query(Product).filter(Product.is_active == True)
        
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        
        return query.offset(skip).limit(limit).all()

    def update_stock(self, db: Session, *, product: Product, new_stock: int) -> Product:
        """
        Update product stock quantity
        
        Args:
            db: Database session
            product: Product instance to update
            new_stock: New stock quantity
            
        Returns:
            Updated product instance
        """
        product.update_stock(new_stock)
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    def decrease_stock(self, db: Session, *, product: Product, quantity: int) -> Product:
        """
        Decrease product stock quantity
        
        Args:
            db: Database session
            product: Product instance to update
            quantity: Quantity to decrease
            
        Returns:
            Updated product instance
            
        Raises:
            ValueError: If insufficient stock
        """
        if product.stock_quantity < quantity:
            raise ValueError("Insufficient stock")
        
        product.decrease_stock(quantity)
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    def increase_stock(self, db: Session, *, product: Product, quantity: int) -> Product:
        """
        Increase product stock quantity
        
        Args:
            db: Database session
            product: Product instance to update
            quantity: Quantity to increase
            
        Returns:
            Updated product instance
        """
        product.increase_stock(quantity)
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    def set_featured(self, db: Session, *, product: Product, is_featured: bool = True) -> Product:
        """
        Set product as featured or not featured
        
        Args:
            db: Database session
            product: Product instance to update
            is_featured: Whether to feature the product
            
        Returns:
            Updated product instance
        """
        product.set_featured(is_featured)
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    def activate_product(self, db: Session, *, product: Product) -> Product:
        """
        Activate a product
        
        Args:
            db: Database session
            product: Product instance to activate
            
        Returns:
            Updated product instance
        """
        product.activate()
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    def deactivate_product(self, db: Session, *, product: Product) -> Product:
        """
        Deactivate a product
        
        Args:
            db: Database session
            product: Product instance to deactivate
            
        Returns:
            Updated product instance
        """
        product.deactivate()
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    def get_low_stock_products(self, db: Session, *, threshold: int = 10, skip: int = 0, limit: int = 100) -> List[Product]:
        """
        Get products with low stock
        
        Args:
            db: Database session
            threshold: Stock quantity threshold
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of products with low stock
        """
        return db.query(Product).filter(
            Product.stock_quantity <= threshold,
            Product.is_active == True
        ).offset(skip).limit(limit).all()

    def get_popular_categories(self, db: Session, *, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get popular product categories
        
        Args:
            db: Database session
            limit: Maximum number of categories to return
            
        Returns:
            List of dictionaries with category and product count
        """
        from sqlalchemy import func
        
        result = db.query(
            Product.category,
            func.count(Product.id).label('product_count')
        ).filter(
            Product.is_active == True
        ).group_by(Product.category).order_by(
            desc(func.count(Product.id))
        ).limit(limit).all()
        
        return [{"category": cat, "product_count": count} for cat, count in result]

    def advanced_search(
        self, 
        db: Session, 
        *,
        name: Optional[str] = None,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        in_stock: Optional[bool] = None,
        is_featured: Optional[bool] = None,
        owner_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Product]:
        """
        Advanced product search with multiple filters
        
        Args:
            db: Database session
            name: Product name to search for
            category: Product category
            min_price: Minimum price
            max_price: Maximum price
            in_stock: Whether product should be in stock
            is_featured: Whether product should be featured
            owner_id: Product owner ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of matching product instances
        """
        query = db.query(Product).filter(Product.is_active == True)
        
        if name:
            query = query.filter(Product.name.contains(name))
        
        if category:
            query = query.filter(Product.category == category)
        
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        
        if in_stock is not None:
            if in_stock:
                query = query.filter(Product.stock_quantity > 0)
            else:
                query = query.filter(Product.stock_quantity == 0)
        
        if is_featured is not None:
            query = query.filter(Product.is_featured == is_featured)
        
        if owner_id is not None:
            query = query.filter(Product.owner_id == owner_id)
        
        return query.offset(skip).limit(limit).all()


# Create a singleton instance
product_repository = ProductRepository()
