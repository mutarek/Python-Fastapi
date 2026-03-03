from fastapi import APIRouter
from fontend.schemas.user import User, UserCreate, CustomResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Dummy in-memory storage
fake_users_db = []

@router.get("/", response_model=CustomResponse[list[User]])
def get_users():
    return CustomResponse(isSuccess=True, statusCode=200, data=fake_users_db)

@router.post("/", response_model=CustomResponse[User])
def create_user(user: UserCreate):
    user_data = User(id=len(fake_users_db)+1, name=user.name, email=user.email, profile=user.profile)
    fake_users_db.append(user_data)
    return CustomResponse(isSuccess=True, statusCode=201, data=user_data)