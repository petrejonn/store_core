import strawberry
from strawberry.fastapi import GraphQLRouter

from store_core.web.gql.context import get_context
from store_core.web.gql import echo
from store_core.web.gql import dummy

@strawberry.type
class Query(  # noqa: WPS215
    echo.Query,
    dummy.Query,
):
    """Main query."""


@strawberry.type
class Mutation(  # noqa: WPS215
    echo.Mutation,
    dummy.Mutation,
):
    """Main mutation."""


schema = strawberry.Schema(
    Query,
    Mutation,
)

gql_router = GraphQLRouter(
    schema,
    graphiql=True,
    context_getter=get_context,
)
