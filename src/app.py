from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from .common.handlers import validation_exception_handler
from .common.middleware import catch_exceptions_middleware
from .routes import core
from .utils.config import Config

config = Config.get()

app = FastAPI()

app.middleware("http")(catch_exceptions_middleware)

cors_kwargs = config.cors_middleware.to_dict()
app.add_middleware(CORSMiddleware, **cors_kwargs)

# exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# routers
app.include_router(core.router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    pass


@app.on_event("shutdown")
async def shutdown_event():
    pass
