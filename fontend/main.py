from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fontend.core.config import get_settings
from fontend.database import Base, engine
from fontend import models
from fontend.routers import user  # import router

settings = get_settings()

app = FastAPI(title=settings.app_name, version=settings.app_version, debug=settings.debug)

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


@app.get("/health")
def health_check():
    return {"status": "ok"}