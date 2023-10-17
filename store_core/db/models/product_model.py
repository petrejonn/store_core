from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy import Index

from store_core.db.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column("id", Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column("name", String(128), nullable=False, unique=True)
    description = Column(String(length=200))

    ix_name = Index('ix_store_products_name', 'name', unique=True)