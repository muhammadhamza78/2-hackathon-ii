"""
Authentication API Endpoints
Handles user registration and login.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.user import User
from app.schemas.auth import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenResponse,
    UserResponse,
)
from app.auth.password import hash_password, verify_password
from app.auth.jwt import create_access_token
from app.config import settings


# ❌ REMOVED prefix="/api/auth"
router = APIRouter(tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    request: UserRegisterRequest,
    session: Session = Depends(get_session),
) -> UserResponse:

    email = request.email.lower().strip()

    existing_user = session.exec(
        select(User).where(User.email == email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    hashed_password = hash_password(request.password)

    user = User(
        email=email,
        hashed_password=hashed_password,
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return UserResponse(
        id=user.id,
        email=user.email,
        created_at=user.created_at,
    )


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    request: UserLoginRequest,
    session: Session = Depends(get_session),
) -> TokenResponse:

    email = request.email.lower().strip()

    user = session.exec(
        select(User).where(User.email == email)
    ).first()

    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    access_token = create_access_token(
        user_id=user.id,
        email=user.email,
    )

    return TokenResponse(
        access_token=access_token,
        token_type="Bearer",
        expires_in=settings.JWT_EXPIRY_HOURS * 3600,
    )
