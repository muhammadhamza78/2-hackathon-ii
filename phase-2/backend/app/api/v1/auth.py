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

<<<<<<< HEAD
    # Generate default name from email if not provided
    display_name = request.name
    if not display_name or display_name.strip() == "":
        # Extract username from email (part before @)
        display_name = email.split("@")[0].replace(".", " ").replace("_", " ").title()

    user = User(
        email=email,
        hashed_password=hashed_password,
        name=display_name,
=======
    user = User(
        email=email,
        hashed_password=hashed_password,
>>>>>>> 09fec55ab4658b42257e6db6376aa6c6353809ac
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return UserResponse(
        id=user.id,
        email=user.email,
<<<<<<< HEAD
        name=user.name,
        profile_picture=user.profile_picture,
=======
>>>>>>> 09fec55ab4658b42257e6db6376aa6c6353809ac
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

<<<<<<< HEAD
    from app.schemas.auth import UserBasicInfo

=======
>>>>>>> 09fec55ab4658b42257e6db6376aa6c6353809ac
    return TokenResponse(
        access_token=access_token,
        token_type="Bearer",
        expires_in=settings.JWT_EXPIRY_HOURS * 3600,
<<<<<<< HEAD
        user=UserBasicInfo(
            id=user.id,
            email=user.email,
            name=user.name,
            profile_picture=user.profile_picture
        )
=======
>>>>>>> 09fec55ab4658b42257e6db6376aa6c6353809ac
    )
