from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, and_
from ..models.product import Product
from ..models.user import User
from ..schemas.product import ProductCreate, ProductUpdate, ProductSearch


class BaseProductService(ABC):
    """
    Abstract base class cho Product Service
    Thể hiện nguyên lý Abstraction trong OOP
    """
    
    @abstractmethod
    def create_product(self, db: Session, product_data: ProductCreate, owner_id: int) -> Product:
        """Tạo sản phẩm mới"""
        pass
    
    @abstractmethod
    def get_product_by_id(self, db: Session, product_id: int) -> Optional[Product]:
        """Lấy sản phẩm theo ID"""
        pass
    
    @abstractmethod
    def search_products(self, db: Session, search_params: ProductSearch) -> List[Product]:
        """Tìm kiếm sản phẩm"""
        pass


class ProductService(BaseProductService):
    """
    Service class cho Product business logic
    Thể hiện các nguyên lý OOP:
    - Encapsulation: Ẩn chi tiết implementation
    - Inheritance: Kế thừa từ BaseProductService
    - Single Responsibility: Chỉ xử lý logic liên quan đến Product
    """
    
    def create_product(self, db: Session, product_data: ProductCreate, owner_id: int) -> Product:
        """
        Tạo sản phẩm mới
        
        Args:
            db: Database session
            product_data: Dữ liệu sản phẩm từ request
            owner_id: ID của user sở hữu sản phẩm
            
        Returns:
            Product: Product object đã được tạo
            
        Raises:
            ValueError: Nếu SKU đã tồn tại hoặc user không tồn tại
        """
        # Kiểm tra user có tồn tại không
        owner = db.query(User).filter(User.id == owner_id).first()
        if not owner:
            raise ValueError("User không tồn tại")
        
        # Kiểm tra SKU đã tồn tại
        if self._sku_exists(db, product_data.sku):
            raise ValueError("SKU đã tồn tại")
        
        # Tạo product object
        product = Product(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            quantity=product_data.quantity,
            sku=product_data.sku,
            category=product_data.category,
            owner_id=owner_id
        )
        
        try:
            db.add(product)
            db.commit()
            db.refresh(product)
            return product
        except IntegrityError:
            db.rollback()
            raise ValueError("Lỗi khi tạo sản phẩm - SKU đã tồn tại")
    
    def get_product_by_id(self, db: Session, product_id: int) -> Optional[Product]:
        """
        Lấy sản phẩm theo ID
        
        Args:
            db: Database session
            product_id: ID của sản phẩm
            
        Returns:
            Optional[Product]: Product object hoặc None
        """
        return db.query(Product).filter(Product.id == product_id).first()
    
    def get_product_by_sku(self, db: Session, sku: str) -> Optional[Product]:
        """
        Lấy sản phẩm theo SKU
        
        Args:
            db: Database session
            sku: SKU của sản phẩm
            
        Returns:
            Optional[Product]: Product object hoặc None
        """
        return db.query(Product).filter(Product.sku == sku).first()
    
    def update_product(self, db: Session, product_id: int, product_data: ProductUpdate, 
                      user_id: int) -> Optional[Product]:
        """
        Cập nhật sản phẩm
        
        Args:
            db: Database session
            product_id: ID của sản phẩm
            product_data: Dữ liệu cập nhật
            user_id: ID của user (để kiểm tra quyền)
            
        Returns:
            Optional[Product]: Product object đã cập nhật hoặc None
            
        Raises:
            PermissionError: Nếu user không có quyền cập nhật
        """
        product = self.get_product_by_id(db, product_id)
        if not product:
            return None
        
        # Kiểm tra quyền sở hữu
        if product.owner_id != user_id:
            raise PermissionError("Bạn không có quyền cập nhật sản phẩm này")
        
        # Cập nhật các fields
        update_data = product_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(product, field):
                setattr(product, field, value)
        
        try:
            db.commit()
            db.refresh(product)
            return product
        except IntegrityError:
            db.rollback()
            raise ValueError("Lỗi khi cập nhật sản phẩm")
    
    def delete_product(self, db: Session, product_id: int, user_id: int) -> bool:
        """
        Xóa sản phẩm
        
        Args:
            db: Database session
            product_id: ID của sản phẩm
            user_id: ID của user (để kiểm tra quyền)
            
        Returns:
            bool: True nếu thành công, False nếu sản phẩm không tồn tại
            
        Raises:
            PermissionError: Nếu user không có quyền xóa
        """
        product = self.get_product_by_id(db, product_id)
        if not product:
            return False
        
        # Kiểm tra quyền sở hữu
        if product.owner_id != user_id:
            raise PermissionError("Bạn không có quyền xóa sản phẩm này")
        
        db.delete(product)
        db.commit()
        return True
    
    def get_products_list(self, db: Session, skip: int = 0, limit: int = 100,
                         owner_id: Optional[int] = None) -> List[Product]:
        """
        Lấy danh sách sản phẩm với pagination
        
        Args:
            db: Database session
            skip: Số record bỏ qua
            limit: Số record tối đa
            owner_id: ID của owner (optional, để lọc theo owner)
            
        Returns:
            List[Product]: Danh sách sản phẩm
        """
        query = db.query(Product)
        
        if owner_id:
            query = query.filter(Product.owner_id == owner_id)
        
        return query.offset(skip).limit(limit).all()
    
    def search_products(self, db: Session, search_params: ProductSearch,
                       skip: int = 0, limit: int = 100) -> List[Product]:
        """
        Tìm kiếm sản phẩm theo các tiêu chí
        
        Args:
            db: Database session
            search_params: Các tham số tìm kiếm
            skip: Số record bỏ qua
            limit: Số record tối đa
            
        Returns:
            List[Product]: Danh sách sản phẩm tìm được
        """
        query = db.query(Product)
        
        # Tìm theo tên
        if search_params.name:
            query = query.filter(Product.name.ilike(f"%{search_params.name}%"))
        
        # Tìm theo danh mục
        if search_params.category:
            query = query.filter(Product.category.ilike(f"%{search_params.category}%"))
        
        # Tìm theo khoảng giá
        if search_params.min_price is not None:
            query = query.filter(Product.price >= search_params.min_price)
        
        if search_params.max_price is not None:
            query = query.filter(Product.price <= search_params.max_price)
        
        # Tìm theo trạng thái
        if search_params.status:
            query = query.filter(Product.status == search_params.status.value)
        
        # Tìm sản phẩm nổi bật
        if search_params.is_featured is not None:
            query = query.filter(Product.is_featured == search_params.is_featured)
        
        return query.offset(skip).limit(limit).all()
    
    def update_stock(self, db: Session, product_id: int, quantity_change: int,
                    user_id: int) -> Optional[Product]:
        """
        Cập nhật tồn kho
        
        Args:
            db: Database session
            product_id: ID của sản phẩm
            quantity_change: Số lượng thay đổi (dương để thêm, âm để giảm)
            user_id: ID của user (để kiểm tra quyền)
            
        Returns:
            Optional[Product]: Product object đã cập nhật hoặc None
            
        Raises:
            PermissionError: Nếu user không có quyền
            ValueError: Nếu số lượng không đủ để giảm
        """
        product = self.get_product_by_id(db, product_id)
        if not product:
            return None
        
        # Kiểm tra quyền sở hữu
        if product.owner_id != user_id:
            raise PermissionError("Bạn không có quyền cập nhật tồn kho sản phẩm này")
        
        # Cập nhật tồn kho
        if quantity_change > 0:
            product.add_stock(quantity_change)
        else:
            success = product.remove_stock(abs(quantity_change))
            if not success:
                raise ValueError("Không đủ hàng trong kho")
        
        db.commit()
        db.refresh(product)
        return product
    
    def get_featured_products(self, db: Session, limit: int = 10) -> List[Product]:
        """
        Lấy danh sách sản phẩm nổi bật
        
        Args:
            db: Database session
            limit: Số lượng sản phẩm tối đa
            
        Returns:
            List[Product]: Danh sách sản phẩm nổi bật
        """
        return db.query(Product).filter(
            and_(Product.is_featured == True, Product.quantity > 0)
        ).limit(limit).all()
    
    def get_products_by_category(self, db: Session, category: str,
                                skip: int = 0, limit: int = 100) -> List[Product]:
        """
        Lấy sản phẩm theo danh mục
        
        Args:
            db: Database session
            category: Tên danh mục
            skip: Số record bỏ qua
            limit: Số record tối đa
            
        Returns:
            List[Product]: Danh sách sản phẩm trong danh mục
        """
        return db.query(Product).filter(
            Product.category.ilike(f"%{category}%")
        ).offset(skip).limit(limit).all()
    
    def get_product_count(self, db: Session, owner_id: Optional[int] = None) -> int:
        """
        Đếm tổng số sản phẩm
        
        Args:
            db: Database session
            owner_id: ID của owner (optional)
            
        Returns:
            int: Số lượng sản phẩm
        """
        query = db.query(Product)
        
        if owner_id:
            query = query.filter(Product.owner_id == owner_id)
        
        return query.count()
    
    def _sku_exists(self, db: Session, sku: str) -> bool:
        """
        Private method kiểm tra SKU đã tồn tại
        Thể hiện Encapsulation - ẩn implementation detail
        
        Args:
            db: Database session
            sku: SKU cần kiểm tra
            
        Returns:
            bool: True nếu SKU đã tồn tại
        """
        return db.query(Product).filter(Product.sku == sku).first() is not None


# Singleton instance
product_service = ProductService()
