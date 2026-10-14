<<<<<<< HEAD
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import HTTPAuthorizationCredentials

from database import get_db
from models import User
from schemas import UserCreate, UserResponse, LoginRequest, Token
from security import (
    hash_password,
    verify_password,
    create_access_token,
    bearer_scheme,
    get_current_user_id
)
=======
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import jwt

import models
from database import SessionLocal
from schemas import UserCreate, UserResponse, LoginRequest, Token
>>>>>>> origin/main


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)


# =========================
<<<<<<< HEAD
=======
# CONFIGURATION
# =========================

SECRET_KEY = "smartevent-secret-key-change-this-to-a-long-random-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

security = HTTPBearer()


# =========================
# DATABASE
# =========================

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# =========================
# PASSWORD FUNCTIONS
# =========================

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


# =========================
# JWT TOKEN
# =========================

def create_access_token(user):
    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "user_id": user.id,
        "role": user.role,
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# =========================
# CURRENT USER
# =========================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user = (
        db.query(models.User)
        .filter(models.User.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user


# =========================
# ROLE CHECK
# =========================

def require_role(*allowed_roles):

    def role_checker(
        current_user: models.User = Depends(get_current_user)
    ):

        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource"
            )

        return current_user

    return role_checker


# =========================
>>>>>>> origin/main
# REGISTER
# =========================

@router.post(
    "/register",
    response_model=UserResponse,
<<<<<<< HEAD
    status_code=status.HTTP_201_CREATED
=======
    status_code=201
>>>>>>> origin/main
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):

<<<<<<< HEAD
    existing_email = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    existing_username = db.query(User).filter(
        User.username == user_data.username
    ).first()

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
=======
    existing_email = (
        db.query(models.User)
        .filter(models.User.email == user_data.email)
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    existing_username = (
        db.query(models.User)
        .filter(models.User.username == user_data.username)
        .first()
    )

    if existing_username:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    user = models.User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        role="USER"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
>>>>>>> origin/main


# =========================
# LOGIN
# =========================

@router.post(
    "/login",
    response_model=Token
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):

<<<<<<< HEAD
    user = db.query(User).filter(
        User.email == login_data.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
=======
    user = (
        db.query(models.User)
        .filter(models.User.email == login_data.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
>>>>>>> origin/main
            detail="Invalid email or password"
        )

    if not verify_password(
        login_data.password,
        user.hashed_password
    ):
        raise HTTPException(
<<<<<<< HEAD
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
=======
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(user)

    return {
        "access_token": token,
>>>>>>> origin/main
        "token_type": "bearer"
    }


# =========================
<<<<<<< HEAD
# USER PROFILE
=======
# GET PROFILE
>>>>>>> origin/main
# =========================

@router.get(
    "/me",
    response_model=UserResponse
)
def get_profile(
<<<<<<< HEAD
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db)
):

    user_id = get_current_user_id(credentials)

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user
=======
    current_user: models.User = Depends(get_current_user)
):

    return current_user
>>>>>>> origin/main
