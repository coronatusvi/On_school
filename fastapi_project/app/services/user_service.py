from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate, UserResponse
from ..crud.user import user_repository
from ..core.security import security_manager
from ..core.exceptions import (
    ValidationException, ConflictException, ResourceNotFoundException,
    DatabaseException
)


class BaseUserService(ABC):
    """
    Abstract base class for User Service
    Implements the Interface Segregation Principle (SOLID)
    """
    
    @abstractmethod
    def create_user(self, db: Session, *, user_data: UserCreate) -> User:
        """Create a new user"""
        pass
    
    @abstractmethod
    def get_user_by_id(self, db: Session, *, user_id: int) -> Optional[User]:
        """Get user by ID"""
        pass
    
    @abstractmethod
    def authenticate_user(self, db: Session, *, username: str, password: str) -> Optional[User]:
        """Authenticate user"""
        pass


class UserService(BaseUserService):
    """
    User Service implementing business logic using Repository Pattern
    
    This class follows SOLID principles:
    - Single Responsibility: Handles user business logic only
    - Open/Closed: Can be extended without modification
    - Liskov Substitution: Can replace BaseUserService
    - Interface Segregation: Specific interfaces for specific operations
    - Dependency Inversion: Depends on Repository abstraction
    """
    
    def __init__(self):
        """Initialize service with dependencies"""
        self.user_repo = user_repository
        self.security = security_manager
    
    def create_user(self, db: Session, *, user_data: UserCreate) -> User:
        """
        Create a new user with business logic validation
        
        Args:
            db: Database session
            user_data: User creation data
            
        Returns:
            Created user instance
            
        Raises:
            ConflictException: If username or email already exists
            ValidationException: If validation fails
            DatabaseException: If database operation fails
        """
        try:
            # Check if username already exists
            if self.user_repo.is_username_taken(db, username=user_data.username):
                raise ConflictException(f"Username '{user_data.username}' is already taken")
            
            # Check if email already exists
            if self.user_repo.is_email_taken(db, email=user_data.email):
                raise ConflictException(f"Email '{user_data.email}' is already registered")
            
            # Hash password
            hashed_password = self.security.hash_password(user_data.password)
            
            # Create user through repository
            user = self.user_repo.create_user(
                db, 
                user_in=user_data, 
                hashed_password=hashed_password
            )
            
            return user
            
        except IntegrityError as e:
            raise ConflictException("User with this username or email already exists")
        except Exception as e:
            raise DatabaseException(f"Failed to create user: {str(e)}")
    
    def get_user_by_id(self, db: Session, *, user_id: int) -> Optional[User]:
        """
        Get user by ID with error handling
        
        Args:
            db: Database session
            user_id: User ID to search for
            
        Returns:
            User instance or None if not found
        """
        try:
            return self.user_repo.get(db, id=user_id)
        except Exception as e:
            raise DatabaseException(f"Failed to get user: {str(e)}")
    
    def get_user_by_id_or_404(self, db: Session, *, user_id: int) -> User:
        """
        Get user by ID or raise 404 exception
        
        Args:
            db: Database session
            user_id: User ID to search for
            
        Returns:
            User instance
            
        Raises:
            ResourceNotFoundException: If user not found
        """
        user = self.get_user_by_id(db, user_id=user_id)
        if not user:
            raise ResourceNotFoundException(f"User with ID {user_id} not found")
        return user
    
    def authenticate_user(self, db: Session, *, username: str, password: str) -> Optional[User]:
        """
        Authenticate user with username/email and password
        
        Args:
            db: Database session
            username: Username or email
            password: Plain text password
            
        Returns:
            User instance if authentication successful, None otherwise
        """
        try:
            # Get user by username or email
            user = self.user_repo.get_by_username_or_email(db, identifier=username)
            
            if not user:
                return None
            
            # Verify password
            if not self.security.verify_password(password, user.hashed_password):
                return None
            
            # Check if user is active
            if not user.is_active:
                return None
            
            return user
            
        except Exception as e:
            raise DatabaseException(f"Authentication failed: {str(e)}")
    
    def update_user(self, db: Session, *, user: User, user_update: UserUpdate) -> User:
        """
        Update user information
        
        Args:
            db: Database session
            user: User instance to update
            user_update: Update data
            
        Returns:
            Updated user instance
            
        Raises:
            ConflictException: If username or email conflicts
            ValidationException: If validation fails
        """
        try:
            update_data = user_update.dict(exclude_unset=True)
            
            # Check username conflict
            if "username" in update_data:
                if self.user_repo.is_username_taken(
                    db, 
                    username=update_data["username"], 
                    exclude_user_id=user.id
                ):
                    raise ConflictException(f"Username '{update_data['username']}' is already taken")
            
            # Check email conflict
            if "email" in update_data:
                if self.user_repo.is_email_taken(
                    db, 
                    email=update_data["email"], 
                    exclude_user_id=user.id
                ):
                    raise ConflictException(f"Email '{update_data['email']}' is already registered")
            
            # Update user through repository
            return self.user_repo.update(db, db_obj=user, obj_in=update_data)
            
        except IntegrityError as e:
            raise ConflictException("Username or email already exists")
        except Exception as e:
            raise DatabaseException(f"Failed to update user: {str(e)}")
    
    def change_password(self, db: Session, *, user: User, current_password: str, new_password: str) -> User:
        """
        Change user password
        
        Args:
            db: Database session
            user: User instance
            current_password: Current plain text password
            new_password: New plain text password
            
        Returns:
            Updated user instance
            
        Raises:
            ValidationException: If current password is incorrect
        """
        # Verify current password
        if not self.security.verify_password(current_password, user.hashed_password):
            raise ValidationException("Current password is incorrect")
        
        # Hash new password
        hashed_password = self.security.hash_password(new_password)
        
        # Update password through repository
        return self.user_repo.update_password(db, user=user, hashed_password=hashed_password)
    
    def get_users_list(
        self, 
        db: Session, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        search: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> List[User]:
        """
        Get list of users with filtering
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            search: Search query for username, email, or full name
            is_active: Filter by active status
            
        Returns:
            List of user instances
        """
        try:
            if search:
                return self.user_repo.search_users(db, query=search, skip=skip, limit=limit)
            
            filters = {}
            if is_active is not None:
                filters["is_active"] = is_active
            
            return self.user_repo.get_multi(db, skip=skip, limit=limit, filters=filters)
            
        except Exception as e:
            raise DatabaseException(f"Failed to get users list: {str(e)}")
    
    def activate_user(self, db: Session, *, user: User) -> User:
        """
        Activate user account
        
        Args:
            db: Database session
            user: User instance to activate
            
        Returns:
            Updated user instance
        """
        try:
            return self.user_repo.activate_user(db, user=user)
        except Exception as e:
            raise DatabaseException(f"Failed to activate user: {str(e)}")
    
    def deactivate_user(self, db: Session, *, user: User) -> User:
        """
        Deactivate user account
        
        Args:
            db: Database session
            user: User instance to deactivate
            
        Returns:
            Updated user instance
        """
        try:
            return self.user_repo.deactivate_user(db, user=user)
        except Exception as e:
            raise DatabaseException(f"Failed to deactivate user: {str(e)}")
    
    def delete_user(self, db: Session, *, user_id: int) -> bool:
        """
        Delete user account
        
        Args:
            db: Database session
            user_id: User ID to delete
            
        Returns:
            True if deletion successful
            
        Raises:
            ResourceNotFoundException: If user not found
        """
        try:
            user = self.get_user_by_id_or_404(db, user_id=user_id)
            deleted_user = self.user_repo.delete(db, id=user_id)
            return deleted_user is not None
            
        except Exception as e:
            raise DatabaseException(f"Failed to delete user: {str(e)}")
    
    def get_user_stats(self, db: Session) -> Dict[str, Any]:
        """
        Get user statistics
        
        Args:
            db: Database session
            
        Returns:
            Dictionary with user statistics
        """
        try:
            total_users = self.user_repo.count(db)
            active_users = self.user_repo.count(db, filters={"is_active": True})
            inactive_users = total_users - active_users
            superusers = self.user_repo.count(db, filters={"is_superuser": True})
            
            return {
                "total_users": total_users,
                "active_users": active_users,
                "inactive_users": inactive_users,
                "superusers": superusers
            }
            
        except Exception as e:
            raise DatabaseException(f"Failed to get user stats: {str(e)}")


# Create a singleton instance
user_service = UserService()
