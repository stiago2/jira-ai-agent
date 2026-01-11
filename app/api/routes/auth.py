"""
Authentication routes.

Provides endpoints for:
- User registration
- User login (JWT token generation)
- Get current user info
- Logout (client-side token deletion)
"""
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.core.encryption import encrypt_token, decrypt_token
from app.models.user import User

router = APIRouter()


# ============================================================================
# Pydantic Models
# ============================================================================

class UserRegister(BaseModel):
    """Request model for user registration."""
    email: EmailStr = Field(..., description="Email address")
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    password: str = Field(..., min_length=8, description="Password (minimum 8 characters)")

    # Jira credentials (optional - can be configured later)
    jira_email: Optional[EmailStr] = Field(None, description="Jira account email (optional)")
    jira_api_token: Optional[str] = Field(None, description="Jira API token (optional)")
    jira_base_url: Optional[str] = Field(None, description="Jira instance URL (optional)")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "password": "SecurePassword123!"
            }
        }


class Token(BaseModel):
    """Response model for login."""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")


class UserResponse(BaseModel):
    """Response model for user information."""
    id: int
    email: str
    username: str
    jira_email: Optional[str] = None
    jira_base_url: Optional[str] = None
    is_active: bool
    is_superuser: bool
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class UpdateJiraCredentials(BaseModel):
    """Request model for updating Jira credentials."""
    jira_email: EmailStr = Field(..., description="Jira account email")
    jira_api_token: str = Field(..., min_length=1, description="Jira API token")
    jira_base_url: str = Field(..., description="Jira instance URL")

    class Config:
        json_schema_extra = {
            "example": {
                "jira_email": "john@company.com",
                "jira_api_token": "ATATT3xFfGF0...",
                "jira_base_url": "https://yourcompany.atlassian.net"
            }
        }


# ============================================================================
# Endpoints
# ============================================================================

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user.

    Creates a new user account with encrypted Jira credentials.

    Args:
        user_data: User registration data
        db: Database session

    Returns:
        UserResponse: Created user information (without sensitive data)

    Raises:
        HTTPException 400: If email or username already exists
    """
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email ya registrado"
        )

    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username ya existe"
        )

    # Validate Jira URL format if provided
    if user_data.jira_base_url and not user_data.jira_base_url.startswith(("http://", "https://")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="URL de Jira debe empezar con http:// o https://"
        )

    # Encrypt Jira token if provided
    encrypted_jira_token = None
    if user_data.jira_api_token:
        encrypted_jira_token = encrypt_token(user_data.jira_api_token)

    # Clean Jira URL if provided
    jira_url = None
    if user_data.jira_base_url:
        jira_url = user_data.jira_base_url.rstrip("/")

    # Create new user
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=get_password_hash(user_data.password),
        jira_email=user_data.jira_email,
        jira_api_token=encrypted_jira_token,
        jira_base_url=jira_url,
        is_active=True,
        is_superuser=False
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Return UserResponse explicitly
    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        username=new_user.username,
        jira_email=new_user.jira_email,
        jira_base_url=new_user.jira_base_url,
        is_active=new_user.is_active,
        is_superuser=new_user.is_superuser,
        created_at=new_user.created_at,
        last_login=new_user.last_login
    )


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login with username and password.

    Returns a JWT access token that should be included in the Authorization
    header for protected endpoints.

    Args:
        form_data: OAuth2 password form (username and password)
        db: Database session

    Returns:
        Token: JWT access token and token type

    Raises:
        HTTPException 401: If credentials are invalid
        HTTPException 403: If user is inactive
    """
    # Find user by username
    user = db.query(User).filter(User.username == form_data.username).first()

    # Verify password
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo. Contacta al administrador."
        )

    # Update last login timestamp
    user.last_login = datetime.utcnow()
    db.commit()

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "username": user.username},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get information about the currently authenticated user.

    Requires valid JWT token in Authorization header.

    Args:
        current_user: Current authenticated user (injected by dependency)

    Returns:
        UserResponse: Current user information
    """
    return current_user


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """
    Logout endpoint.

    Since JWT is stateless, logout is handled client-side by deleting the token.
    This endpoint exists for consistency and can be extended for token blacklisting.

    Args:
        current_user: Current authenticated user (injected by dependency)

    Returns:
        dict: Success message
    """
    return {
        "message": "Logout exitoso",
        "detail": "Por favor, elimina el token del cliente"
    }


@router.put("/jira-credentials", response_model=UserResponse)
async def update_jira_credentials(
    credentials: UpdateJiraCredentials,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update Jira credentials for the current user.

    Allows users to configure or update their Jira integration credentials
    after registration.

    Args:
        credentials: New Jira credentials
        current_user: Current authenticated user
        db: Database session

    Returns:
        UserResponse: Updated user information

    Raises:
        HTTPException 400: If Jira URL format is invalid
    """
    # Validate Jira URL format
    if not credentials.jira_base_url.startswith(("http://", "https://")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="URL de Jira debe empezar con http:// o https://"
        )

    # Update user's Jira credentials
    current_user.jira_email = credentials.jira_email
    current_user.jira_api_token = encrypt_token(credentials.jira_api_token)
    current_user.jira_base_url = credentials.jira_base_url.rstrip("/")

    db.commit()
    db.refresh(current_user)

    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        jira_email=current_user.jira_email,
        jira_base_url=current_user.jira_base_url,
        is_active=current_user.is_active,
        is_superuser=current_user.is_superuser,
        created_at=current_user.created_at,
        last_login=current_user.last_login
    )


@router.get("/health")
async def auth_health_check():
    """
    Health check endpoint for authentication service.

    Returns:
        dict: Health status
    """
    return {
        "service": "authentication",
        "status": "healthy"
    }
