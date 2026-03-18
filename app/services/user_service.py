from sqlalchemy.orm import Session

from ..core.exceptions import BadRequestError, UnauthorizedError
from ..models import user as user_model
from ..schemas import user as user_schema
from ..utils.hash import hash_password, verify_password


def get_user_by_email(db: Session, email: str):
    return db.query(user_model.User).filter(user_model.User.email == email).first()


def create_user(db: Session, user_data: user_schema.UserCreate):
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        raise BadRequestError("Email already registered")

    new_user = user_model.User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        raise UnauthorizedError("Invalid credentials")
    return user
