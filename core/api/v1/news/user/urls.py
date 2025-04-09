from ninja import Router

from core.api.v1.news.user.handlers import router as client_router


router = Router(tags=['Clients'])

router.add_router(prefix="client/", router=client_router)
