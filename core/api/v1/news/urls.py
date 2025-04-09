from ninja import Router

from core.api.v1.news.user.urls import router as client_router

router = Router(tags=['news'])
router.add_router('user/', client_router)

