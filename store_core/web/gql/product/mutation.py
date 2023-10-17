import strawberry

from store_core.db.dao.product_dao import ProductDAO
from store_core.web.gql.context import Context

from strawberry.types import Info

@strawberry.type
class Mutation:
    """Mutations for product."""

    @strawberry.mutation(description="Create product object in a database")
    async def create_product(
        self,
        info: Info[Context, None],
        name: str,
        descriptions: str,
    ) -> str:
        """
        Creates product model in a database.

        :param info: connection info.
        :param name: name of a product.
        :return: name of a product model.
        """
        dao = ProductDAO(info.context.db_connection)
        await dao.create_product(name=name, description=descriptions)
        return name
