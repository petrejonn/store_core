from fastapi import Depends
from strawberry.fastapi import BaseContext
from sqlalchemy.ext.asyncio import AsyncSession
from store_core.db.dependencies import get_db_session


class Context(BaseContext):
    """Global graphql context."""

    def __init__(
        self,
        db_connection: AsyncSession = Depends(get_db_session),
    ) -> None:
        self.db_connection = db_connection
        pass  # noqa: WPS420


def get_context(context: Context = Depends(Context)) -> Context:
    """
    Get custom context.

    :param context: graphql context.
    :return: context
    """
    return context
