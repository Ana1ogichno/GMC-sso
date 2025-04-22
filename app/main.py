from fastapi import FastAPI, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from starlette.middleware.sessions import SessionMiddleware

from app.config.dependencies.exception import (
    get_exception_handler,
    get_exception_middleware,
    get_validation_exception_handler
)
from app.config.docs.dependencies import get_tags_metadata, get_app_description
from app.config.exception import (
    BackendException,
)
from app.config.settings import settings
from app.router import api_router


# === Constants === #
origins = [
    "*"
]

# === Dependency Injection === #
tags_metadata = get_tags_metadata()
app_description = get_app_description()


# Exception Handling Dependencies
backend_exception_handler = get_exception_handler()
handle_exceptions_middleware = get_exception_middleware()
validation_exception_handler = get_validation_exception_handler()


# === FastAPI App Initialization === #
app = FastAPI(
    debug=True,
    title=settings.project.PROJECT_NAME,
    version=settings.project.PROJECT_VERSION,
    openapi_url=f"{settings.project.API_V1_STR}/openapi.json",
    openapi_tags=tags_metadata.get_tags_metadata(),
    exception_handlers={BackendException: backend_exception_handler.handle},
    description=app_description.build_description(),
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,
        "docExpansion": "none",
    },
)


# === Middleware Setup === #
def setup_middleware():
    """
    Configures middleware for CORS and session handling.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(SessionMiddleware, secret_key=settings.project.OAUTH_SECRET_KEY)
    app.middleware("http")(handle_exceptions_middleware)  # Global exception handling middleware

    app.exception_handler(RequestValidationError)(validation_exception_handler.handle)


# === Router Setup === #
def include_routers():
    """
    Includes all application routes with API versioning.
    """
    app.include_router(api_router, prefix=settings.project.API_V1_STR)


# === Pagination Setup === #
def setup_pagination():
    """
    Sets up pagination for FastAPI endpoints.
    """
    add_pagination(app)


# === Initialize App Configuration === #
def initialize_app():
    """
    Calls all setup functions to configure the application.
    """
    setup_middleware()
    include_routers()
    setup_pagination()


# === Run App Initialization === #
initialize_app()
