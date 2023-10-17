from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String

from store_core.db.base import Base

class Store(Base):
    __tablename__ = "stores"

    id = Column("id", Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column("name", String(256), nullable=False, index=True, unique=True)
    schema = Column("schema", String(256), nullable=False, unique=True)
    host = Column("host", String(256), nullable=False, unique=True)
    phone = Column("phone", String(256), nullable=False, unique=True)

    __table_args__ = ({"schema": "shared"},)