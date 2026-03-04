from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from fontend.database import get_db
from fontend.schemas.user import User, UserCreate, UserUpdate, CustomResponse
from fontend.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/", response_model=CustomResponse[list[User]])
def get_users(
    db: Session = Depends(get_db),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
):
    users = UserService.list_users(db, skip=skip, limit=limit)
    return CustomResponse(isSuccess=True, statusCode=200, data=users)


@router.get("/{user_id}", response_model=CustomResponse[User])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user_data = UserService.get_user_or_404(db, user_id)
    return CustomResponse(isSuccess=True, statusCode=200, data=user_data)

@router.post("/", response_model=CustomResponse[User])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_data = UserService.create_user(db, user)
    return CustomResponse(isSuccess=True, statusCode=201, data=user_data)


@router.put("/{user_id}", response_model=CustomResponse[User])
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    user_data = UserService.update_user(db, user_id, user)
    return CustomResponse(isSuccess=True, statusCode=200, data=user_data)


@router.delete("/{user_id}", response_model=CustomResponse[dict[str, str]])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    UserService.delete_user(db, user_id)
    return CustomResponse(
        isSuccess=True,
        statusCode=200,
        data={"message": "User deleted successfully"},
    )