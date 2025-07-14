    #!/usr/bin/env python3
"""
Script để test kết nối database và khởi tạo dữ liệu mẫu
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import db_manager, get_database
from app.core.config import settings
from app.models.user import User
from app.models.product import Product
from app.services.user_service import user_service
from app.services.product_service import product_service
from app.schemas.user import UserCreate
from app.schemas.product import ProductCreate


def test_database_connection():
    """Test kết nối database"""
    print("🔍 Testing database connection...")
    
    try:
        # Test engine
        engine = db_manager.engine
        print(f"✅ Database engine created: {engine}")
        
        # Test connection
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            print(f"✅ Database connection successful: {result.fetchone()}")
        
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def create_tables():
    """Tạo tất cả các bảng"""
    print("📋 Creating database tables...")
    
    try:
        db_manager.create_tables()
        print("✅ Tables created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create tables: {e}")
        return False


def create_sample_data():
    """Tạo dữ liệu mẫu"""
    print("📝 Creating sample data...")
    
    try:
        # Lấy database session
        db_gen = get_database()
        db = next(db_gen)
        
        # Tạo user mẫu
        sample_users = [
            UserCreate(
                username="admin",
                email="admin@example.com",
                password="Admin123!",
                full_name="Administrator"
            ),
            UserCreate(
                username="john_doe",
                email="john@example.com", 
                password="Password123!",
                full_name="John Doe"
            )
        ]
        
        created_users = []
        for user_data in sample_users:
            try:
                user = user_service.create_user(db, user_data)
                created_users.append(user)
                print(f"✅ Created user: {user.username}")
            except ValueError as e:
                print(f"⚠️  User {user_data.username} already exists")
                # Lấy user existing
                existing_user = user_service.get_user_by_username(db, user_data.username)
                if existing_user:
                    created_users.append(existing_user)
        
        # Tạo sản phẩm mẫu
        if created_users:
            admin_user = created_users[0]
            sample_products = [
                ProductCreate(
                    name="Laptop Dell XPS 13",
                    description="Laptop cao cấp với màn hình 4K",
                    price=25000000.0,
                    quantity=10,
                    sku="DELL-XPS13-001",
                    category="Electronics"
                ),
                ProductCreate(
                    name="iPhone 14 Pro",
                    description="Điện thoại Apple mới nhất",
                    price=30000000.0,
                    quantity=5,
                    sku="APPLE-IP14P-001",
                    category="Mobile"
                ),
                ProductCreate(
                    name="MacBook Pro M2",
                    description="Laptop Apple với chip M2",
                    price=45000000.0,
                    quantity=3,
                    sku="APPLE-MBP-M2-001",
                    category="Electronics"
                )
            ]
            
            for product_data in sample_products:
                try:
                    product = product_service.create_product(db, product_data, admin_user.id)
                    print(f"✅ Created product: {product.name}")
                except ValueError as e:
                    print(f"⚠️  Product {product_data.name} already exists")
        
        print("✅ Sample data created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create sample data: {e}")
        return False
    finally:
        db.close()


def main():
    """Main function"""
    print("🚀 FastAPI Database Setup")
    print("=" * 50)
    print(f"Database URL: {settings.database_url}")
    print(f"App Name: {settings.app_name}")
    print("=" * 50)
    
    # Test connection
    if not test_database_connection():
        sys.exit(1)
    
    # Create tables
    if not create_tables():
        sys.exit(1)
    
    # Create sample data
    if not create_sample_data():
        sys.exit(1)
    
    print("\n🎉 Database setup completed successfully!")
    print("\n📚 Next steps:")
    print("1. Run the FastAPI server: uvicorn app.main:app --reload")
    print("2. Open browser: http://localhost:8000/docs")
    print("3. Login with admin/Admin123! to test API")


if __name__ == "__main__":
    main()
