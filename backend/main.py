"""FastAPI AI Ecosystem Gateway API entrypoint."""

import time
import traceback
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.app.core.config import settings
from backend.db.database import Base, engine
from backend.app.models import DatasetModel, ModelRegistryModel, UserModel  # noqa: F401
from backend.app.routers import auth, datasets, health, inference, models, train
from backend.app.utils.logger import logger

app = FastAPI(
    title="FastAPI AI Ecosystem Gateway API",
    version="1.0.0",
    description="Central API Gateway for AI Inference & System Management",
)

# CORS Configuration
origins = settings.cors_origins if isinstance(settings.cors_origins, list) else [settings.cors_origins]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Request/Response & Error Logging Middleware."""
    start_time = time.time()
    client_host = request.client.host if request.client else "unknown"
    response = await call_next(request)
    process_time = time.time() - start_time
    duration_ms = int(process_time * 1000)

    log_extra = {
        "path": request.url.path,
        "method": request.method,
        "status_code": response.status_code,
        "client_ip": client_host,
        "duration_ms": duration_ms,
        "operation": f"{request.method} {request.url.path}",
        "status": "SUCCESS" if response.status_code < 400 else "FAIL",
    }

    log_msg = f"{request.method} {request.url.path} HTTP/{request.scope.get('http_version', '1.1')} {response.status_code} - {duration_ms}ms"

    if response.status_code >= 500:
        logger.error(log_msg, extra=log_extra)
    elif response.status_code >= 400:
        logger.warning(log_msg, extra=log_extra)
    else:
        logger.info(log_msg, extra=log_extra)

    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global Unhandled Exception Handler."""
    logger.error(
        "Unhandled Exception on %s %s: %s",
        request.method,
        request.url.path,
        str(exc),
        exc_info=True,
        extra={
            "path": request.url.path,
            "method": request.method,
            "error_detail": str(exc),
            "traceback": traceback.format_exc(),
        },
    )
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """HTTP Exception Handler."""
    logger.warning(
        "HTTPException [%s] on %s %s: %s",
        exc.status_code,
        request.method,
        request.url.path,
        exc.detail,
        extra={
            "status_code": exc.status_code,
            "path": request.url.path,
            "method": request.method,
            "error_detail": exc.detail,
        },
    )
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Request Validation Error Handler."""
    logger.warning(
        "Validation Error [422] on %s %s: %s",
        request.method,
        request.url.path,
        str(exc.errors()),
        extra={
            "status_code": 422,
            "path": request.url.path,
            "method": request.method,
            "error_detail": exc.errors(),
        },
    )
    return JSONResponse(status_code=422, content={"detail": exc.errors()})


@app.on_event("startup")
def startup_event():
    """Execute startup database initialization."""
    logger.info("Ensuring database tables exist...", extra={"operation": "startup", "status": "INFO"})
    Base.metadata.create_all(bind=engine)
    logger.info("FastAPI AI Ecosystem Gateway API successfully started", extra={"operation": "startup", "status": "SUCCESS"})


# Include API Routers
app.include_router(auth.router)
app.include_router(datasets.router)
app.include_router(models.router)
app.include_router(train.router)
app.include_router(inference.router)
app.include_router(health.router)


@app.get("/")
def root():
    """Gateway Root API endpoint."""
    return {"message": "Welcome to FastAPI AI Ecosystem Gateway API"}

