from os import name
from typing import List

from fastapi import APIRouter
from fastapi.param_functions import Depends

from store_core.db.dao.store_dao import StoreDAO
from store_core.db.models.store_model import Store
from store_core.web.api.store.schema import StoreDTO, StoreInputDTO

router = APIRouter()


@router.get("/", response_model=List[StoreDTO])
async def get_stores(
    limit: int = 10,
    offset: int = 0,
    store_dao: StoreDAO = Depends(),
) -> List[Store]:
    """
    Retrieve all store objects from the database.

    :param limit: limit of store objects, defaults to 10.
    :param offset: offset of store objects, defaults to 0.
    :param store_dao: DAO for store models.
    :return: list of store obbjects from database.
    """
    return await store_dao.get_all_stores(limit=limit, offset=offset)


@router.post("/")
async def create_store(
    new_store_object: StoreInputDTO,
    store_dao: StoreDAO = Depends(),
) -> None:
    """
    Creates store model in the database.

    :param new_store_object: new store model item.
    :param store_dao: DAO for store models.
    """
    await store_dao.create_store(name=new_store_object.name, host=f'{new_store_object.name}.localhost', schema=new_store_object.name, phone=new_store_object.phone)