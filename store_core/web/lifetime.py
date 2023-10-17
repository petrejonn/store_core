from typing import Awaitable, Callable
import logging
from fastapi import FastAPI

from store_core.settings import settings
from store_core.db.meta import meta
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import (
    SERVICE_NAME,
    TELEMETRY_SDK_LANGUAGE,
    DEPLOYMENT_ENVIRONMENT,
    Resource,
)
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import set_tracer_provider
from opentelemetry.instrumentation.sqlalchemy import (
    SQLAlchemyInstrumentor,
)
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from asyncio import current_task
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker
from alembic.runtime.migration import MigrationContext
from alembic.config import Config as alembic_config
from alembic import command
import sqlalchemy as sa

def get_shared_metadata():
    shared_meta = sa.MetaData()
    for table in meta.tables.values():
        if table.schema != "store":
            table.tometadata(shared_meta)
    return shared_meta

async def _setup_db(app: FastAPI) -> None:
    engine = create_async_engine(str(settings.db_url), echo=settings.db_echo)
    session_factory = async_scoped_session(
        sessionmaker(engine, expire_on_commit=False, class_=AsyncSession),
        scopefunc=current_task,
    )
    app.state.db_engine = engine
    app.state.db_session_factory = session_factory

    async with engine.begin() as conn:
        def do_sync(sync_conn):
            context = MigrationContext.configure(sync_conn)
            if context.get_current_revision() is not None:
                print("Database already exists.")
                return
            sa.schema.CreateSchema("shared").execute(sync_conn)
            get_shared_metadata().create_all(bind=sync_conn)
            alembic_config.attributes["connection"] = sync_conn
            command.stamp(alembic_config, "head", purge=True)

        await conn.run_sync(do_sync)




def setup_opentelemetry(app: FastAPI) -> None:  # pragma: no cover
    """
    Enables opentelemetry instrumentation.

    :param app: current application.
    """
    if not settings.opentelemetry_endpoint:
        return

    tracer_provider = TracerProvider(
        resource=Resource(
            attributes={
                SERVICE_NAME: "store_core",
                TELEMETRY_SDK_LANGUAGE: "python",
                DEPLOYMENT_ENVIRONMENT: settings.environment,
            }
        )
    )

    tracer_provider.add_span_processor(
        BatchSpanProcessor(
            OTLPSpanExporter(
                endpoint=settings.opentelemetry_endpoint,
                insecure=True,
            )
        )
    )

    excluded_endpoints = [
        app.url_path_for('health_check'),
        app.url_path_for('openapi'),
        app.url_path_for('swagger_ui_html'),
        app.url_path_for('swagger_ui_redirect'),
        app.url_path_for('redoc_html'),
    ]

    FastAPIInstrumentor().instrument_app(
        app,
        tracer_provider=tracer_provider,
        excluded_urls=",".join(excluded_endpoints),
    )
    SQLAlchemyInstrumentor().instrument(
        tracer_provider=tracer_provider,
        engine=app.state.db_engine.sync_engine,
    )
    LoggingInstrumentor().instrument(
        tracer_provider=tracer_provider,
        set_logging_format=True,
        log_level=logging.getLevelName(settings.log_level.value),
    )

    set_tracer_provider(tracer_provider=tracer_provider)


def stop_opentelemetry(app: FastAPI) -> None:  # pragma: no cover
    """
    Disables opentelemetry instrumentation.

    :param app: current application.
    """
    if not settings.opentelemetry_endpoint:
        return

    FastAPIInstrumentor().uninstrument_app(app)
    SQLAlchemyInstrumentor().uninstrument()


def register_startup_event(app: FastAPI) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application startup.

    This function uses fastAPI app to store data
    inthe state, such as db_engine.

    :param app: the fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("startup")
    async def _startup() -> None:  # noqa: WPS430
        await _setup_db(app)
        setup_opentelemetry(app)
        pass  # noqa: WPS420

    return _startup


def register_shutdown_event(app: FastAPI) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application's shutdown.

    :param app: fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("shutdown")
    async def _shutdown() -> None:  # noqa: WPS430
        await app.state.db_engine.dispose()
        
        stop_opentelemetry(app)
        pass  # noqa: WPS420

    return _shutdown
