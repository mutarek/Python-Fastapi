from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fontend.database import Base, engine
from fontend.models.user import User as UserModel
from fontend.routers import user  # import router

app = FastAPI(title="FastTime API 🚀", version="1.0.0")

Base.metadata.create_all(bind=engine)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = {}
    for error in exc.errors():
        field = error["loc"][-1]  # get the field name (last part of location)
        errors[field] = error["msg"]

    return JSONResponse(
        status_code=422,
        content={
            "isSuccess": False,
            "statusCode": 422,
            "errors": errors,
        },
    )

# Include all routers
app.include_router(user.router)