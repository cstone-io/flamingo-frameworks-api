import os

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from .common.handlers import validation_exception_handler
from .common.middleware import catch_exceptions_middleware

app = FastAPI()

app.middleware("http")(catch_exceptions_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ["CORS_ALLOW_ORIGINS"].split(","),
    allow_credentials=os.environ["CORS_ALLOW_CREDENTIALS"] == "true",
    allow_methods=os.environ["CORS_ALLOW_METHODS"].split(","),
    allow_headers=os.environ["CORS_ALLOW_HEADERS"].split(","),
)

# exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# routers
app.include_router() # TODO: implement


@app.on_event("startup")
async def startup_event():
    pass

@app.on_event("shutdown")
async def shutdown_event():
    pass
