import hashlib

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from fontend.database import get_db
from fontend.models.user import User as UserModel
from fontend.schemas.user import User, UserCreate, UserUpdate, CustomResponse

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


@router.put("/{user_id}", response_model=CustomResponse[User])
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    user_data = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

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
        user_data.hashed_password = hashlib.sha256(user.password.encode()).hexdigest()

    db.commit()
    db.refresh(user_data)
    return CustomResponse(isSuccess=True, statusCode=200, data=user_data)


@router.delete("/{user_id}", response_model=CustomResponse[dict[str, str]])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_data = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user_data)
    db.commit()
    return CustomResponse(
        isSuccess=True,
        statusCode=200,
        data={"message": "User deleted successfully"},
    )