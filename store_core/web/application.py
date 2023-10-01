from fastapi import FastAPI
from fastapi.responses import UJSONResponse
import logging
from store_core.web.api.router import api_router
from store_core.settings import settings
from store_core.web.gql.router import gql_router
from store_core.web.lifetime import register_startup_event, register_shutdown_event
from importlib import metadata


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="store_core",
        version=metadata.version("store_core"),
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")
    # Graphql router
    app.include_router(router=gql_router, prefix="/graphql")

    return app
