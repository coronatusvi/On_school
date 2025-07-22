"""
Custom exceptions và error handlers cho FastAPI application
Thể hiện nguyên lý OOP trong exception handling
"""

from fastapi import HTTPException, status
from typing import Optional, Dict, Any


class BaseAPIException(Exception):
    """
    Base exception class cho tất cả custom exceptions
    Thể hiện nguyên lý Inheritance trong OOP
    """
    
    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
                 details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationException(BaseAPIException):
    """
    Exception cho validation errors
    """
    
    def __init__(self, message: str = "Dữ liệu không hợp lệ", 
                 details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details
        )


class AuthenticationException(BaseAPIException):
    """
    Exception cho authentication errors
    """
    
    def __init__(self, message: str = "Xác thực thất bại", 
                 details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            details=details
        )


class AuthorizationException(BaseAPIException):
    """
    Exception cho authorization errors
    """
    
    def __init__(self, message: str = "Không có quyền truy cập", 
                 details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            details=details
        )


class ResourceNotFoundException(BaseAPIException):
    """
    Exception cho resource not found errors
    """
    
    def __init__(self, resource: str = "tài nguyên", 
                 details: Optional[Dict[str, Any]] = None):
        message = f"{resource.capitalize()} không tồn tại"
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            details=details
        )


class ConflictException(BaseAPIException):
    """
    Exception cho conflict errors (duplicate data, etc.)
    """
    
    def __init__(self, message: str = "Dữ liệu đã tồn tại", 
                 details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            details=details
        )


class DatabaseException(BaseAPIException):
    """
    Exception cho database errors
    """
    
    def __init__(self, message: str = "Lỗi cơ sở dữ liệu", 
                 details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details
        )


class BusinessLogicException(BaseAPIException):
    """
    Exception cho business logic errors
    """
    
    def __init__(self, message: str = "Lỗi logic nghiệp vụ", 
                 details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details
        )


class ErrorHandler:
    """
    Class xử lý error handling cho ứng dụng
    Thể hiện nguyên lý Encapsulation và Single Responsibility
    """
    
    @staticmethod
    def handle_database_error(error: Exception) -> DatabaseException:
        """
        Xử lý database errors
        
        Args:
            error: Exception gốc
            
        Returns:
            DatabaseException: Custom database exception
        """
        error_msg = str(error)
        
        if "UNIQUE constraint failed" in error_msg:
            return ConflictException("Dữ liệu đã tồn tại trong hệ thống")
        elif "FOREIGN KEY constraint failed" in error_msg:
            return ValidationException("Dữ liệu tham chiếu không hợp lệ")
        elif "NOT NULL constraint failed" in error_msg:
            return ValidationException("Thiếu dữ liệu bắt buộc")
        else:
            return DatabaseException(f"Lỗi cơ sở dữ liệu: {error_msg}")
    
    @staticmethod
    def handle_validation_error(error: Exception) -> ValidationException:
        """
        Xử lý validation errors
        
        Args:
            error: Exception gốc
            
        Returns:
            ValidationException: Custom validation exception
        """
        return ValidationException(
            message="Dữ liệu không hợp lệ",
            details={"error": str(error)}
        )
    
    @staticmethod
    def handle_auth_error(error: Exception) -> AuthenticationException:
        """
        Xử lý authentication errors
        
        Args:
            error: Exception gốc
            
        Returns:
            AuthenticationException: Custom auth exception
        """
        return AuthenticationException(
            message="Xác thực thất bại",
            details={"error": str(error)}
        )
    
    @staticmethod
    def to_http_exception(api_exception: BaseAPIException) -> HTTPException:
        """
        Chuyển đổi custom exception thành HTTPException
        
        Args:
            api_exception: Custom API exception
            
        Returns:
            HTTPException: FastAPI HTTPException
        """
        return HTTPException(
            status_code=api_exception.status_code,
            detail={
                "message": api_exception.message,
                "details": api_exception.details,
                "error_type": api_exception.__class__.__name__
            }
        )


# Global error handler instance
error_handler = ErrorHandler()

# Aliases for backward compatibility
UnauthorizedException = AuthorizationException
