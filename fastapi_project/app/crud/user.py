from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_

from .base import BaseRepository
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    """
    User Repository implementing specific user operations
    
    Inherits from BaseRepository and adds user-specific methods
    following the Repository Pattern and SOLID principles
    """

    def __init__(self):
        super().__init__(User)

    def get_by_field(self, db: Session, *, field: str, value: str) -> Optional[User]:
        """
        Get user by any field (implementation of abstract method)
        
        Args:
            db: Database session
            field: Field name to search by
            value: Value to search for
            
        Returns:
            User instance or None if not found
        """
        if hasattr(User, field):
            return db.query(User).filter(getattr(User, field) == value).first()
        return None

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """
        Get user by email address
        
        Args:
            db: Database session
            email: Email address to search for
            
        Returns:
            User instance or None if not found
        """
        return db.query(User).filter(User.email == email).first()

    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        """
        Get user by username
        
        Args:
            db: Database session
            username: Username to search for
            
        Returns:
            User instance or None if not found
        """
        return db.query(User).filter(User.username == username).first()

    def get_by_username_or_email(self, db: Session, *, identifier: str) -> Optional[User]:
        """
        Get user by username or email (useful for login)
        
        Args:
            db: Database session
            identifier: Username or email to search for
            
        Returns:
            User instance or None if not found
        """
        return db.query(User).filter(
            or_(User.username == identifier, User.email == identifier)
        ).first()

    def create_user(self, db: Session, *, user_in: UserCreate, hashed_password: str) -> User:
        """
        Create a new user with hashed password
        
        Args:
            db: Database session
            user_in: User creation schema
            hashed_password: Already hashed password
            
        Returns:
            Created user instance
        """
        user_data = user_in.dict()
        user_data["hashed_password"] = hashed_password
        user_data.pop("password", None)  # Remove plain password if exists
        
        db_user = User(**user_data)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def update_password(self, db: Session, *, user: User, hashed_password: str) -> User:
        """
        Update user's password
        
        Args:
            db: Database session
            user: User instance to update
            hashed_password: New hashed password
            
        Returns:
            Updated user instance
        """
        user.hashed_password = hashed_password
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def activate_user(self, db: Session, *, user: User) -> User:
        """
        Activate a user account
        
        Args:
            db: Database session
            user: User instance to activate
            
        Returns:
            Updated user instance
        """
        user.activate()
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def deactivate_user(self, db: Session, *, user: User) -> User:
        """
        Deactivate a user account
        
        Args:
            db: Database session
            user: User instance to deactivate
            
        Returns:
            Updated user instance
        """
        user.deactivate()
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def get_active_users(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Get all active users
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of active user instances
        """
        return db.query(User).filter(User.is_active == True).offset(skip).limit(limit).all()

    def get_superusers(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Get all superusers
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of superuser instances
        """
        return db.query(User).filter(User.is_superuser == True).offset(skip).limit(limit).all()

    def search_users(self, db: Session, *, query: str, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Search users by username, email, or full name
        
        Args:
            db: Database session
            query: Search query string
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of matching user instances
        """
        search_filter = or_(
            User.username.contains(query),
            User.email.contains(query),
            User.full_name.contains(query)
        )
        
        return db.query(User).filter(search_filter).offset(skip).limit(limit).all()

    def is_username_taken(self, db: Session, *, username: str, exclude_user_id: Optional[int] = None) -> bool:
        """
        Check if username is already taken
        
        Args:
            db: Database session
            username: Username to check
            exclude_user_id: User ID to exclude from check (for updates)
            
        Returns:
            True if username is taken, False otherwise
        """
        query = db.query(User).filter(User.username == username)
        
        if exclude_user_id:
            query = query.filter(User.id != exclude_user_id)
        
        return query.first() is not None

    def is_email_taken(self, db: Session, *, email: str, exclude_user_id: Optional[int] = None) -> bool:
        """
        Check if email is already taken
        
        Args:
            db: Database session
            email: Email to check
            exclude_user_id: User ID to exclude from check (for updates)
            
        Returns:
            True if email is taken, False otherwise
        """
        query = db.query(User).filter(User.email == email)
        
        if exclude_user_id:
            query = query.filter(User.id != exclude_user_id)
        
        return query.first() is not None


# Create a singleton instance
user_repository = UserRepository()
