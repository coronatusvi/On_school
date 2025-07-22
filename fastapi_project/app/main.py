"""
FastAPI application with Repository Pattern
This is the new main.py using the Repository Pattern architecture

Architecture:
├── main.py (this file)          # FastAPI app configuration
├── models/                      # Pydantic models & SQLAlchemy ORM models
├── crud/                        # Repository/CRUD operations 
├── services/                    # Business logic using CRUD operations
└── api/
    └── v1/
        └── endpoints/           # FastAPI routes using services
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from typing import Any

from .core.database import db_manager, Base
from .core.config import settings
from .core.exceptions import (
    ValidationException, ConflictException, ResourceNotFoundException,
    DatabaseException, UnauthorizedException
)
from .api.v1.api import api_router
import time


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    Handles startup and shutdown events
    """
    # Startup
    logger.info("Starting up FastAPI application with Repository Pattern...")
    
    # Create database tables
    try:
        db_manager.create_tables()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down FastAPI application...")


# Create FastAPI app with lifespan
app = FastAPI(
    title="FastShop API with Repository Pattern",
    description="""
    A modern e-commerce API built with FastAPI using Repository Pattern architecture.
    
    ## Features
    
    * **User Management**: Registration, authentication, profile management
    * **Product Management**: CRUD operations, search, categorization, stock management
    * **Repository Pattern**: Clean separation of concerns with Repository/Service layers
    * **SOLID Principles**: Following SOLID design principles throughout the codebase
    * **Comprehensive Error Handling**: Structured exception handling with custom exceptions
    * **JWT Authentication**: Secure token-based authentication
    * **Input Validation**: Comprehensive request/response validation using Pydantic
    
    ## Architecture
    
    This API follows the Repository Pattern with clear separation of layers:
    
    * **API Layer** (`/api/v1/endpoints/`): FastAPI routes handling HTTP requests
    * **Service Layer** (`/services/`): Business logic and orchestration
    * **Repository Layer** (`/crud/`): Data access and persistence operations
    * **Model Layer** (`/models/`): SQLAlchemy ORM models and Pydantic schemas
    * **Core Layer** (`/core/`): Configuration, database, security, and utilities
    
    ## Authentication
    
    Most endpoints require JWT authentication. To authenticate:
    
    1. Register a new user or login with existing credentials
    2. Use the returned `access_token` in the Authorization header: `Bearer <token>`
    
    ## Error Handling
    
    The API returns structured error responses with appropriate HTTP status codes:
    
    * **400**: Bad Request - Invalid input or business logic violation
    * **401**: Unauthorized - Authentication required or failed
    * **403**: Forbidden - Insufficient permissions
    * **404**: Not Found - Requested resource doesn't exist
    * **409**: Conflict - Resource conflict (e.g., duplicate username)
    * **422**: Unprocessable Entity - Validation errors
    * **500**: Internal Server Error - Unexpected server errors
    """,
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)


# Custom exception handlers
@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException) -> JSONResponse:
    """Handle validation exceptions"""
    logger.warning(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc), "type": "validation_error"}
    )


@app.exception_handler(ConflictException)
async def conflict_exception_handler(request: Request, exc: ConflictException) -> JSONResponse:
    """Handle conflict exceptions"""
    logger.warning(f"Conflict error: {exc}")
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc), "type": "conflict_error"}
    )


@app.exception_handler(ResourceNotFoundException)
async def not_found_exception_handler(request: Request, exc: ResourceNotFoundException) -> JSONResponse:
    """Handle resource not found exceptions"""
    logger.warning(f"Resource not found: {exc}")
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc), "type": "not_found_error"}
    )


@app.exception_handler(UnauthorizedException)
async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException) -> JSONResponse:
    """Handle unauthorized exceptions"""
    logger.warning(f"Unauthorized access: {exc}")
    return JSONResponse(
        status_code=403,
        content={"detail": str(exc), "type": "unauthorized_error"}
    )


@app.exception_handler(DatabaseException)
async def database_exception_handler(request: Request, exc: DatabaseException) -> JSONResponse:
    """Handle database exceptions"""
    logger.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "type": "database_error"}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions"""
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "type": "unexpected_error"}
    )


# Include API routers
app.include_router(api_router, prefix="/api/v1")


# Health check endpoint
@app.get("/", tags=["health"])
async def root() -> Any:
    """
    Root endpoint for health check
    """
    return {
        "message": "FastShop API with Repository Pattern",
        "version": "2.0.0",
        "status": "healthy",
        "architecture": "Repository Pattern",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["health"])
async def health_check() -> Any:
    """
    Health check endpoint
    """
    try:
        # Test database connection
        db_session = next(db_manager.get_session())
        db_session.execute("SELECT 1")
        db_session.close()
        
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")


# Add startup event logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests for debugging"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.4f}s"
    )
    
    return response


if __name__ == "__main__":
    import uvicorn
    import time
    
    uvicorn.run(
        "app.main_new:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
