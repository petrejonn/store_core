from typing import Optional
import strawberry


@strawberry.type
class ProductDTO:
    """
    DTO for product models.

    It returned when accessing product models from the API.
    """

    id: int
    name: str
    description: Optional[str]