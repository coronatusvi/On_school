from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .core.config import settings
from .core.database import db_manager
from .routers import auth, users, products


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager cho lifecycle của ứng dụng
    Khởi tạo database khi start và cleanup khi shutdown
    """
    # Startup
    print("🚀 Starting FastAPI application...")
    print(f"📦 App: {settings.app_name} v{settings.version}")
    
    # Tạo các bảng database
    db_manager.create_tables()
    print("✅ Database tables created")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down FastAPI application...")


class FastAPIApp:
    """
    Class chính của ứng dụng FastAPI
    Thể hiện nguyên lý OOP trong việc tổ chức ứng dụng
    - Encapsulation: Ẩn chi tiết cấu hình
    - Single Responsibility: Chỉ chịu trách nhiệm khởi tạo app
    """
    
    def __init__(self):
        """
        Constructor khởi tạo FastAPI app với cấu hình
        """
        self.app = FastAPI(
            title=settings.app_name,
            version=settings.version,
            debug=settings.debug,
            description=self._get_description(),
            lifespan=lifespan
        )
        
        self._configure_middleware()
        self._register_routers()
    
    def _get_description(self) -> str:
        """
        Private method để tạo description cho API
        Thể hiện Encapsulation
        """
        return """
        ## FastAPI Project - Ôn tập OOP và Router

        Dự án FastAPI đầy đủ để thực hành các khái niệm:
        
        ### 🔧 Kiến trúc
        - **Object-Oriented Programming (OOP)**: Classes, inheritance, encapsulation, polymorphism
        - **Dependency Injection**: FastAPI dependencies cho database, authentication
        - **Service Layer Pattern**: Tách biệt business logic khỏi API layer
        - **Repository Pattern**: Quản lý data access thông qua models
        
        ### 🛡️ Bảo mật
        - **JWT Authentication**: Token-based authentication
        - **Password Hashing**: Bcrypt password hashing
        - **Role-based Access**: User permissions và ownership
        
        ### 📊 Database
        - **SQLAlchemy ORM**: Object-relational mapping
        - **Relationships**: User-Product one-to-many relationship
        - **Migrations**: Database schema management
        
        ### 🚀 API Features
        - **CRUD Operations**: Create, Read, Update, Delete
        - **Search & Filter**: Advanced product search
        - **Pagination**: Efficient data pagination
        - **Validation**: Pydantic data validation
        """
    
    def _configure_middleware(self):
        """
        Private method để cấu hình middleware
        Thể hiện Encapsulation
        """
        # CORS middleware để cho phép frontend gọi API
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Trong production nên cấu hình cụ thể
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def _register_routers(self):
        """
        Private method để đăng ký các router
        Thể hiện Encapsulation và Composition
        """
        # Đăng ký các router với prefix
        self.app.include_router(auth.router)
        self.app.include_router(users.router)
        self.app.include_router(products.router)
    
    def get_app(self) -> FastAPI:
        """
        Public method để lấy FastAPI app instance
        
        Returns:
            FastAPI: Configured FastAPI application
        """
        return self.app


# Root endpoint
@asynccontextmanager
async def get_app_with_routes():
    """Factory function để tạo app với tất cả routes"""
    app_instance = FastAPIApp()
    app = app_instance.get_app()
    
    @app.get("/", tags=["Root"])
    async def root():
        """
        Root endpoint để kiểm tra API hoạt động
        """
        return {
            "message": "🎉 Welcome to FastAPI OOP Practice Project!",
            "app_name": settings.app_name,
            "version": settings.version,
            "docs_url": "/docs",
            "redoc_url": "/redoc",
            "features": [
                "JWT Authentication",
                "User Management", 
                "Product Management",
                "Advanced Search",
                "OOP Design Patterns",
                "Service Layer Architecture"
            ]
        }
    
    @app.get("/health", tags=["Health"])
    async def health_check():
        """
        Health check endpoint
        """
        return {
            "status": "healthy",
            "app": settings.app_name,
            "version": settings.version
        }
    
    yield app


# Tạo instance của ứng dụng
app_factory = FastAPIApp()
app = app_factory.get_app()


# Root routes
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint để kiểm tra API hoạt động
    """
    return {
        "message": "🎉 Welcome to FastAPI OOP Practice Project!",
        "app_name": settings.app_name,
        "version": settings.version,
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "features": [
            "JWT Authentication",
            "User Management", 
            "Product Management",
            "Advanced Search",
            "OOP Design Patterns",
            "Service Layer Architecture"
        ]
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.version
    }
