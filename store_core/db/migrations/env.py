import asyncio
from logging.config import fileConfig

import sqlalchemy as sa
from alembic import context
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy.future import Connection

from store_core.db.meta import meta
from store_core.db.models import load_all_models
from store_core.settings import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config


load_all_models()
# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = meta

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


async def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=str(settings.db_url),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def include_name(name, type_, parent_names):
    if type_ == "schema":
        # this **will* include the default schema
        return name in [None, "shared", "store_default", "store"]
    else:
        return True
    

def do_run_migrations(connection: Connection) -> None:
    """
    Run actual sync migrations.

    :param connection: connection to the database.
    """
    # Create a new MetaData object
    translated = sa.MetaData()

    # Define a function to translate the schema
    def translate_schema(table):
        # If the original schema is 'shop', change it to 'shop_default'
        if table.schema == 'store':
            return 'store_default'
        # Otherwise, keep the original schema
        return table.schema

    # Copy all tables from target_metadata to translated, changing the schema if necessary
    for table in target_metadata.tables.values():
        table.tometadata(translated, schema=translate_schema(table))

    context.configure(connection=connection, target_metadata=translated, compare_type=True,
            transaction_per_migration=True,
            include_schemas=True,include_name = include_name,)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = create_async_engine(str(settings.db_url))

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

loop = asyncio.get_event_loop()
if context.is_offline_mode():
    task = run_migrations_offline()
else:
    task = run_migrations_online()

loop.run_until_complete(task)
