from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import AccountAPI, MyTokenObtainPairView

account_router = DefaultRouter()
account_router.register('', AccountAPI, basename='account')

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('token-verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', include(account_router.urls)),
]
