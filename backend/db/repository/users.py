import sqlite3

from core.hashing import Hasher
from db.models.users import User
from schemas.users import UserCreate
from sqlalchemy.orm import Session


def create_new_user(user: UserCreate, db_session: Session):
    user = User(
        username=user.username,
        email=user.email,
        hashed_password=Hasher.get_password_hash(user.password),
        is_active=True,
        is_superuser=False,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


def get_user_by_email(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    return user
