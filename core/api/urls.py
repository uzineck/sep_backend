from django.urls import path
from ninja import NinjaAPI
from ninja.throttling import AnonRateThrottle, AuthRateThrottle

from core.api.v1.urls import router as v1_router


api = NinjaAPI(
    title="CHMNU NEWS",
    description="This is an api for CHMNU NEWS",
    csrf=True,
    throttle=[
        AnonRateThrottle('10/s'),
        AuthRateThrottle('50/s'),
    ],
)


api.add_router('v1/', v1_router)

urlpatterns = [
    path('', api.urls),
]
