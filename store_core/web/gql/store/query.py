from typing import List

import strawberry
from strawberry.types import Info

from store_core.db.dao.store_dao import StoreDAO
from store_core.web.gql.context import Context
from store_core.web.gql.store.schema import StoreDTO


@strawberry.type
class Query:
    """Query to interact with stores."""

    @strawberry.field(description="Get all stores")
    async def get_stores(
        self,
        info: Info[Context, None],
        limit: int = 15,
        offset: int = 0,
    ) -> List[StoreDTO]:
        """
        Retrieves all store objects from database.

        :param info: connection info.
        :param limit: limit of store objects, defaults to 10.
        :param offset: offset of store objects, defaults to 0.
        :return: list of store obbjects from database.
        """
        dao = StoreDAO(info.context.db_connection)
        return await dao.get_all_stores(limit=limit, offset=offset)  # type: ignore
