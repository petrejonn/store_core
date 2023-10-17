from typing import List, Optional
from fastapi import Depends
import sqlalchemy as sa
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from alembic.runtime.migration import MigrationContext
from alembic.config import Config
from alembic.script import ScriptDirectory

from store_core.db.dependencies import get_db_session
from store_core.db.models.store_model import Store
from store_core.db.utils import get_store_specific_metadata


class StoreDAO:
    """Class for accessing store table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_store(self, name: str, schema: str, host: str, phone:str) -> None:
        """ Add single store to session.
        :param name: name of a store.
        """
        async with self.session.begin():
            connection = await self.session.connection()

            def create_tables_and_add_store(conn):
                context = MigrationContext.configure(conn)
                alembic_config = Config('alembic.ini')
                script = ScriptDirectory.from_config(alembic_config)

                if context.get_current_revision() != script.get_current_head():
                    raise RuntimeError(
                        "Database is not up-to-date. Execute migrations before adding new stores."
                    )

                # Create new schema
                conn.execute(sa.schema.CreateSchema(f'store_{schema}'))

                # Get store-specific metadata
                store_meta = get_store_specific_metadata()

                # Change schema of all tables in store_meta to the new schema
                for table in store_meta.tables.values():
                    table.schema = f'store_{schema}'

                # Add store to session
                self.session.add(Store(name=name, host=host, schema=f'store_{schema}', phone=phone))

                # Create all tables in the new schema
                store_meta.create_all(bind=conn)

            await connection.run_sync(create_tables_and_add_store)


    async def get_all_stores(self, limit: int, offset: int) -> List[Store]:
        """
        Get all store models with limit/offset pagination.

        :param limit: limit of stores.
        :param offset: offset of stores.
        :return: stream of stores.
        """
        raw_stores = await self.session.execute(
            select(Store).limit(limit).offset(offset),
        )

        return raw_stores.scalars().fetchall()

    async def filter(
        self,
        name: Optional[str] = None
    ) -> List[Store]:
        """
        Get specific store model.

        :param name: name of store instance.
        :return: store models.
        """
        query = select(Store)
        if name:
            query = query.where(Store.name == name)
        rows = await self.session.execute(query)
        return rows.scalars().fetchall()
