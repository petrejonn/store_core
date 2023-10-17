from typing import List, Optional
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from store_core.db.dependencies import get_db_session, get_store_db_session
from store_core.db.models.product_model import Product


class ProductDAO:
    """Class for accessing product table."""

    def __init__(self, session: AsyncSession = Depends(get_store_db_session)):
        self.session = session

    async def create_product(self, name: str, description: str) -> None:
        """
        Add single product to session.

        :param name: name of a product.
        """
        self.session.add(Product(name=name, description=description))

    async def get_all_products(self, limit: int, offset: int) -> List[Product]:
        """
        Get all product models with limit/offset pagination.

        :param limit: limit of product.
        :param offset: offset of product.
        :return: stream of product.
        """
        raw_products = await self.session.execute(
            select(Product).limit(limit).offset(offset),
        )

        return raw_products.scalars().fetchall()

    async def filter(
        self,
        name: Optional[str] = None
    ) -> List[Product]:
        """
        Get specific product model.

        :param name: name of product instance.
        :return: product models.
        """
        query = select(Product)
        if name:
            query = query.where(Product.name == name)
        rows = await self.session.execute(query)
        return rows.scalars().fetchall()
