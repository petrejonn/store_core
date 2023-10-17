import functools
from typing import Callable

from sqlalchemy import text
from typeguard import typechecked
from alembic import op


@typechecked
def for_each_tenant_schema(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapped():
        stmt = text("SELECT schema FROM shared.stores")
        schemas = op.get_bind().execute(stmt).fetchall()
        for (schema,) in schemas:
            func(schema)

    return wrapped