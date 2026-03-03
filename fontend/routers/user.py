import hashlib

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from fontend.database import get_db
from fontend.models.user import User as UserModel
from fontend.schemas.user import User, UserCreate, CustomResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/", response_model=CustomResponse[list[User]])
def get_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return CustomResponse(isSuccess=True, statusCode=200, data=users)

@router.post("/", response_model=CustomResponse[User])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_data = UserModel(
        name=user.name,
        email=user.email,
        profile=user.profile,
        hashed_password=hashlib.sha256(user.password.encode()).hexdigest(),
    )
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    return CustomResponse(isSuccess=True, statusCode=201, data=user_data)