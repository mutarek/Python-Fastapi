from fastapi import HTTPException
from sqlalchemy.orm import Session

from fontend.core.security import hash_password
from fontend.models.user import User as UserModel
from fontend.schemas.user import UserCreate, UserUpdate


class UserService:
    @staticmethod
    def list_users(db: Session, skip: int = 0, limit: int = 20):
        return db.query(UserModel).offset(skip).limit(limit).all()

    @staticmethod
    def get_user_or_404(db: Session, user_id: int):
        user_data = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")
        return user_data

    @staticmethod
    def create_user(db: Session, user: UserCreate):
        existing_user = db.query(UserModel).filter(UserModel.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        user_data = UserModel(
            name=user.name,
            email=user.email,
            profile=user.profile,
            hashed_password=hash_password(user.password),
        )
        db.add(user_data)
        db.commit()
        db.refresh(user_data)
        return user_data

    @staticmethod
    def update_user(db: Session, user_id: int, user: UserUpdate):
        user_data = UserService.get_user_or_404(db, user_id)

        if user.email and user.email != user_data.email:
            existing_user = db.query(UserModel).filter(UserModel.email == user.email).first()
            if existing_user:
                raise HTTPException(status_code=400, detail="Email already registered")

        if user.name is not None:
            user_data.name = user.name
        if user.email is not None:
            user_data.email = user.email
        if user.profile is not None:
            user_data.profile = user.profile
        if user.password is not None:
            user_data.hashed_password = hash_password(user.password)

        db.commit()
        db.refresh(user_data)
        return user_data

    @staticmethod
    def delete_user(db: Session, user_id: int):
        user_data = UserService.get_user_or_404(db, user_id)
        db.delete(user_data)
        db.commit()