from datetime import datetime, timedelta
from typing import Union, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from .config import settings


class SecurityManager:
    """
    Lớp quản lý bảo mật sử dụng OOP
    Encapsulation: Ẩn chi tiết implementation của mã hóa và JWT
    """
    
    def __init__(self):
        # Khởi tạo context cho mã hóa mật khẩu
        try:
            self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            self.secret_key = settings.secret_key
            self.algorithm = settings.algorithm
            self.access_token_expire_minutes = settings.access_token_expire_minutes
            
            # Validate secret key
            if not self.secret_key or len(self.secret_key) < 32:
                raise ValueError("Secret key must be at least 32 characters long")
                
        except Exception as e:
            print(f"❌ Failed to initialize SecurityManager: {e}")
            raise RuntimeError(f"Security initialization failed: {e}")
    
    def hash_password(self, password: str) -> str:
        """
        Mã hóa mật khẩu
        
        Args:
            password: Mật khẩu cần mã hóa
            
        Returns:
            str: Mật khẩu đã được mã hóa
            
        Raises:
            ValueError: Nếu password không hợp lệ
            RuntimeError: Nếu có lỗi khi hash
        """
        try:
            if not password:
                raise ValueError("Password cannot be empty")
            
            if len(password) < 8:
                raise ValueError("Password must be at least 8 characters long")
                
            return self.pwd_context.hash(password)
        except ValueError:
            raise
        except Exception as e:
            print(f"❌ Error hashing password: {e}")
            raise RuntimeError(f"Password hashing failed: {e}")
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Xác thực mật khẩu
        
        Args:
            plain_password: Mật khẩu gốc
            hashed_password: Mật khẩu đã mã hóa
            
        Returns:
            bool: True nếu mật khẩu đúng
            
        Raises:
            ValueError: Nếu input không hợp lệ
        """
        try:
            if not plain_password or not hashed_password:
                raise ValueError("Password and hash cannot be empty")
                
            return self.pwd_context.verify(plain_password, hashed_password)
        except ValueError:
            raise
        except Exception as e:
            print(f"❌ Error verifying password: {e}")
            return False
    
    def create_access_token(self, data: dict, expires_delta: Union[timedelta, None] = None) -> str:
        """
        Tạo JWT access token
        
        Args:
            data: Dữ liệu cần encode vào token
            expires_delta: Thời gian hết hạn (optional)
            
        Returns:
            str: JWT token
            
        Raises:
            ValueError: Nếu data không hợp lệ
            RuntimeError: Nếu có lỗi khi tạo token
        """
        try:
            if not data:
                raise ValueError("Token data cannot be empty")
                
            to_encode = data.copy()
            if expires_delta:
                expire = datetime.utcnow() + expires_delta
            else:
                expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
            
            to_encode.update({"exp": expire})
            encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
            return encoded_jwt
        except ValueError:
            raise
        except Exception as e:
            print(f"❌ Error creating access token: {e}")
            raise RuntimeError(f"Token creation failed: {e}")
    
    def verify_token(self, token: str) -> Union[dict, None]:
        """
        Xác thực và decode JWT token
        
        Args:
            token: JWT token cần xác thực
            
        Returns:
            dict: Payload nếu token hợp lệ, None nếu không hợp lệ
        """
        try:
            if not token:
                return None
                
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            print("⚠️  Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            print(f"⚠️  Invalid token: {e}")
            return None
        except Exception as e:
            print(f"❌ Error verifying token: {e}")
            return None


# Singleton instance
security_manager = SecurityManager()
