# FastAPI Project - Ôn tập OOP và Router

Dự án FastAPI đầy đủ để thực hành các khái niệm:
- Object-Oriented Programming (OOP)
- FastAPI Routers
- Dependency Injection
- Database Models với SQLAlchemy
- Authentication & Authorization
- Pydantic Schemas
- Service Layer Pattern

## Cấu trúc dự án

```
fastapi_project/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py          # Cấu hình ứng dụng
│   │   ├── security.py        # JWT, mã hóa mật khẩu
│   │   └── database.py        # Kết nối database
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py            # User model với OOP
│   │   └── product.py         # Product model với OOP
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py            # Pydantic schemas cho User
│   │   └── product.py         # Pydantic schemas cho Product
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py    # Business logic cho User
│   │   └── product_service.py # Business logic cho Product
│   └── routers/
│       ├── __init__.py
│       ├── auth.py            # Authentication router
│       ├── users.py           # User management router
│       └── products.py        # Product management router
├── requirements.txt
└── README.md
```

## Chạy ứng dụng

```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Setup Database 
cd /fastapi_project && python setup_database.py

# Chạy server
uvicorn app.main:app --reload
```

## API Endpoints

- **Authentication:**
  - POST `/auth/register` - Đăng ký user mới
  - POST `/auth/login` - Đăng nhập
  
- **Users:**
  - GET `/users/me` - Lấy thông tin user hiện tại
  - PUT `/users/me` - Cập nhật thông tin user
  
- **Products:**
  - GET `/products/` - Lấy danh sách sản phẩm
  - POST `/products/` - Tạo sản phẩm mới
  - GET `/products/{id}` - Lấy thông tin sản phẩm
  - PUT `/products/{id}` - Cập nhật sản phẩm
  - DELETE `/products/{id}` - Xóa sản phẩm

## Các khái niệm được thực hành

1. **OOP**: Classes, inheritance, encapsulation trong models và services
2. **Dependency Injection**: FastAPI dependencies cho authentication, database
3. **Router**: Tách biệt logic theo domain
4. **Service Layer**: Tách biệt business logic khỏi API layer
5. **Authentication**: JWT tokens, password hashing
6. **Database**: SQLAlchemy ORM với relationships
