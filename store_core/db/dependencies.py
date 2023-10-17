from typing import AsyncGenerator

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from fastapi import Depends, HTTPException
from starlette.requests import Request
from store_core.db.models.store_model import Store

async def get_store(req: Request) -> Store:
    host_without_port = req.headers["host"].split(":", 1)[0]
    async with req.app.state.db_session_factory() as session:
        stmt = select(Store).where(Store.host == host_without_port)
        result = await session.execute(stmt)
        store = result.scalars().first()
        if store is None:
            raise HTTPException(status_code=404, detail="Store not found")
        return store

async def get_store_db_session(request: Request, store: Store = Depends(get_store)) -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = request.app.state.db_session_factory()
    await session.connection(execution_options={"schema_translate_map": {"store": store.schema}})
    try:
        # Change the current schema
        await session.execute(f"SET search_path TO {store.schema}")
        yield session
    finally:
        await session.commit()
        await session.close()



async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """
    Create and get database session.

    :param request: current request.
    :yield: database session.
    """
    session: AsyncSession = request.app.state.db_session_factory()

    try:  # noqa: WPS501
        yield session
    finally:
        await session.commit()
        await session.close()
