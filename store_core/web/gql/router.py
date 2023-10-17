import strawberry
from strawberry.fastapi import GraphQLRouter

from store_core.web.gql.context import get_context
from store_core.web.gql import product

@strawberry.type
class Query(  # noqa: WPS215
    product.Query,
):
    """Main query."""


@strawberry.type
class Mutation(  # noqa: WPS215
    product.Mutation,
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
