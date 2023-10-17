from fastapi.routing import APIRouter
from store_core.web.api import monitoring
from store_core.web.api import store

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(store.router,prefix="/store", tags=["store"])
