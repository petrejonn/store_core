import strawberry


@strawberry.type
class StoreDTO:
    """
    DTO for store models.

    It returned when accessing store models from the API.
    """

    id: int
    name: str
    host:str
    schema:str
