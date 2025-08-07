"""Url configuration for accounts."""

from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from account.api.views import RegisterView, LoginView

app_name = "account.api"

router = SimpleRouter()
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),

    path("login/", LoginView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]
