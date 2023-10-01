import strawberry

from store_core.db.dao.dummy_dao import DummyDAO
from store_core.web.gql.context import Context

from strawberry.types import Info

@strawberry.type
class Mutation:
    """Mutations for dummies."""

    @strawberry.mutation(description="Create dummy object in a database")
    async def create_dummy_model(
        self,
        info: Info[Context, None],
        name: str,
    ) -> str:
        """
        Creates dummy model in a database.

        :param info: connection info.
        :param name: name of a dummy.
        :return: name of a dummt model.
        """
        dao = DummyDAO(info.context.db_connection)
        await dao.create_dummy_model(name=name)
        return name
