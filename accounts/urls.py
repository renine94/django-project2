from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AccountAPI

account_router = DefaultRouter()
account_router.register('', AccountAPI, basename='account')

urlpatterns = [
    path('', include(account_router.urls)),
]
