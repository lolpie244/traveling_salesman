from django.urls import path
from django.urls.conf import include
from .v1.urls import router as v1_router

urlpatterns = [path('v1/', include((v1_router.urls, 'v1-history')))]

