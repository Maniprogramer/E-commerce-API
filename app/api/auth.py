from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import os
from jose import JWTError, jwt

from ..core.security import create_access_token
from ..db.database import get_db
from ..schemas import user as user_schema
from ..services import user_service
from ..models import user as user_model

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = user_service.get_user_by_email(db, email)
    if user is None:
        raise credentials_exception
    return user

def get_current_admin_user(current_user: user_model.User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    return current_user

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=user_schema.UserResponse)
def signup(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user)

@router.post("/login", response_model=user_schema.TokenResponse)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_service.authenticate_user(db, user_credentials.username, user_credentials.password)
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/profile", response_model=user_schema.UserResponse)
def get_profile(current_user: user_model.User = Depends(get_current_user)):
    return current_user
