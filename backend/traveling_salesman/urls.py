from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.api.urls')),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/blacklist/', jwt_views.TokenBlacklistView.as_view(), name='token_blacklist'),
]

