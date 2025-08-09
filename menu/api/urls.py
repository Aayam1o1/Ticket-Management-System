"""Url configuration for menu."""

from django.urls import path
from rest_framework.routers import SimpleRouter
from menu.api.views import (
    MenuListCreateView,
    MenuRetrieveUpdateDestroyView
)

app_name = "menu.api"

router = SimpleRouter()
urlpatterns = [
    path('list/', MenuListCreateView.as_view(), name='menu-list'),
    path('<int:id>/', MenuRetrieveUpdateDestroyView.as_view(), name='menu-detail'),


]
