# FastAPI Repository Pattern Migration

This document explains the new Repository Pattern architecture and how to use it.

## Architecture Overview

The new architecture follows the Repository Pattern with clear separation of concerns:

```
├── main.py                     # FastAPI app with Repository Pattern (final version)
├── models/                     # SQLAlchemy ORM models (unchanged)
│   ├── user.py
│   └── product.py
├── crud/                       # NEW: Repository layer for data access
│   ├── base.py                 # Base repository with common CRUD operations
│   ├── user.py                 # User repository with specific operations
│   └── product.py              # Product repository with specific operations
├── services/                   # REFACTORED: Business logic using repositories
│   ├── user_service.py         # User service using repository (final version)
│   └── product_service.py      # Product service using repository (final version)
└── api/                        # NEW: API layer with versioning
    └── v1/
        ├── api.py              # Main API router
        └── endpoints/
            ├── users.py        # User endpoints using services
            └── products.py     # Product endpoints using services
```

## Key Benefits

### 1. Separation of Concerns
- **Repository Layer**: Pure data access, no business logic
- **Service Layer**: Business logic, validation, orchestration
- **API Layer**: HTTP handling, request/response transformation

### 2. SOLID Principles
- **Single Responsibility**: Each class has one reason to change
- **Open/Closed**: Easy to extend without modifying existing code
- **Liskov Substitution**: Repository implementations are interchangeable
- **Interface Segregation**: Specific interfaces for specific operations
- **Dependency Inversion**: High-level modules don't depend on low-level modules

### 3. Testability
- Easy to mock repositories for unit testing
- Business logic isolated from data access
- Clear dependencies and injection points

### 4. Maintainability
- Clear code organization
- Easy to find and modify specific functionality
- Reduced coupling between layers

## How to Use

### 1. Start the New Application

```bash
# Run the Repository Pattern version
cd fastapi_project
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Repository Layer Usage

```python
# Example: Using User Repository
from app.crud.user import user_repository
from app.core.database import SessionLocal

db = SessionLocal()

# Create user
user = user_repository.create_user(db, user_in=user_data, hashed_password="...")

# Get user by email
user = user_repository.get_by_email(db, email="test@example.com")

# Search users
users = user_repository.search_users(db, query="john", skip=0, limit=10)

# Check if username is taken
is_taken = user_repository.is_username_taken(db, username="johndoe")
```

### 3. Service Layer Usage

```python
# Example: Using User Service
from app.services.user_service import user_service
from app.schemas.user import UserCreate

# Create user with business logic
user_data = UserCreate(username="johndoe", email="john@example.com", password="secret123")
user = user_service.create_user(db, user_data=user_data)

# Authenticate user
user = user_service.authenticate_user(db, username="johndoe", password="secret123")

# Get user stats
stats = user_service.get_user_stats(db)
```

### 4. API Layer Usage

```python
# Example: API endpoint
from app.services.user_service import user_service

@router.post("/register")
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        user = user_service.create_user(db, user_data=user_data)
        return UserResponse.from_orm(user)
    except ConflictException as e:
        raise HTTPException(status_code=409, detail=str(e))
```

## Migration Guide

### From Old Structure to New Structure

#### 1. Controllers → API Endpoints
```python
# Old: app/routers/users.py
class UserController:
    def register_user(self, db: Session, user_data: UserCreate):
        # Business logic mixed with HTTP handling
        pass

# New: app/api/v1/endpoints/users.py
@router.post("/register")
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Only HTTP handling, business logic in service
    user = user_service.create_user(db, user_data=user_data)
    return UserResponse.from_orm(user)
```

#### 2. Services → Repository + Service
```python
# Old: app/services/user_service.py
class UserService:
    def create_user(self, db: Session, user_data: UserCreate):
        # Mixed data access and business logic
        user = User(**user_data.dict())
        db.add(user)
        db.commit()
        return user

# New: Split into Repository + Service
# app/crud/user.py
class UserRepository:
    def create_user(self, db: Session, user_in: UserCreate, hashed_password: str):
        # Pure data access
        pass

# app/services/user_service.py
class UserService:
    def create_user(self, db: Session, user_data: UserCreate):
        # Business logic only
        hashed_password = self.security.hash_password(user_data.password)
        return self.user_repo.create_user(db, user_in=user_data, hashed_password=hashed_password)
```

## API Documentation

### New Endpoints Structure

#### Users API (`/api/v1/users/`)
- `POST /register` - Register new user
- `POST /login` - User login
- `GET /me` - Get current user info
- `PUT /me` - Update current user
- `POST /change-password` - Change password
- `GET /` - List users (with filtering)
- `GET /{user_id}` - Get user by ID
- `PUT /{user_id}/activate` - Activate user (admin)
- `PUT /{user_id}/deactivate` - Deactivate user (admin)
- `DELETE /{user_id}` - Delete user (admin)
- `GET /stats/overview` - User statistics (admin)

#### Products API (`/api/v1/products/`)
- `POST /` - Create product
- `GET /` - List products (with filtering)
- `GET /featured` - Get featured products
- `GET /category/{category}` - Get products by category
- `GET /my-products` - Get current user's products
- `POST /search` - Advanced product search
- `GET /{product_id}` - Get product by ID
- `PUT /{product_id}` - Update product
- `DELETE /{product_id}` - Delete product
- `PATCH /{product_id}/stock` - Update stock
- `PATCH /{product_id}/featured` - Set featured status
- `GET /stats/categories` - Popular categories
- `GET /stats/overview` - Product statistics
- `GET /stats/low-stock` - Low stock products

## Error Handling

The new architecture includes comprehensive error handling:

```python
# Custom Exceptions
ValidationException      # 422 - Validation errors
ConflictException       # 409 - Resource conflicts
ResourceNotFoundException # 404 - Resource not found
UnauthorizedException   # 403 - Insufficient permissions
DatabaseException       # 500 - Database errors
```

## Testing

### Unit Testing Examples

```python
# Test Repository
def test_user_repository():
    mock_db = Mock()
    user_repo = UserRepository()
    
    # Test repository methods
    user = user_repo.get_by_email(mock_db, email="test@example.com")
    assert user is not None

# Test Service
def test_user_service():
    mock_repo = Mock()
    user_service = UserService()
    user_service.user_repo = mock_repo
    
    # Test business logic
    result = user_service.create_user(mock_db, user_data=user_data)
    mock_repo.create_user.assert_called_once()

# Test API
def test_register_endpoint():
    response = client.post("/api/v1/users/register", json=user_data)
    assert response.status_code == 201
```

## Performance Considerations

### 1. Repository Pattern Benefits
- **Caching**: Easy to add caching at repository level
- **Connection Pooling**: Centralized database connection management
- **Query Optimization**: Specific optimized queries per repository

### 2. Service Layer Benefits
- **Business Logic Caching**: Cache expensive business operations
- **Background Tasks**: Easy to move operations to background
- **Rate Limiting**: Apply rate limits at service level

## Next Steps

1. **Test the new endpoints** using the documentation at `/docs`
2. **Update frontend calls** to use the new API structure
3. **Monitor performance** and add optimizations as needed
4. **Add unit tests** for repositories and services
5. **Consider adding caching** for frequently accessed data

## Rollback Plan

If needed, you can rollback to the old structure:

```bash
# Use the old main.py
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The old files are preserved and can be used as backup.
