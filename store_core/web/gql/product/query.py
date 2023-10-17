from typing import List
from store_core.db.dependencies import get_store_db_session

import strawberry
from strawberry.types import Info

from store_core.db.dao.product_dao import ProductDAO
from store_core.web.gql.context import Context
from store_core.web.gql.product.schema import ProductDTO


@strawberry.type
class Query:
    """Query to interact with product."""

    @strawberry.field(description="Get all product")
    async def get_products(
        self,
        info: Info[Context, None],
        limit: int = 15,
        offset: int = 0,
    ) -> List[ProductDTO]:
        """
        Retrieves all product objects from database.

        :param info: connection info.
        :param limit: limit of product objects, defaults to 10.
        :param offset: offset of product objects, defaults to 0.
        :return: list of product obbjects from database.
        """
        dao = ProductDAO(info.context.db_connection)
        return await dao.get_all_products(limit=limit, offset=offset)  # type: ignore
