import strawberry

from store_core.db.dao.store_dao import StoreDAO
from store_core.web.gql.context import Context

from strawberry.types import Info

@strawberry.type
class Mutation:
    """Mutations for stores."""

    @strawberry.mutation(description="Create store object in a database")
    async def create_store(
        self,
        info: Info[Context, None],
        name: str,
        host: str,
        schema: str,
    ) -> str:
        """
        Creates store model in a database.

        :param info: connection info.
        :param name: name of a store.
        :return: name of a store model.
        """
        dao = StoreDAO(info.context.db_connection)
        await dao.create_store(name=name,schema=schema, host=host)
        return name
