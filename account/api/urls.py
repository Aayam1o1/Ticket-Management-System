"""Url configuration for accounts."""

from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from account.api.views import (
    RegisterView,
    LoginView,
    RoleListCreateAPIView,
    PermissionListCreateAPIView,
    PermissionRetrieveUpdateDestroyAPIView,
    RolePermissionListAPIView,
    AssignPermissionsToRoleAPIView,
    RoleRetrieveUpdateDestroyView
)

app_name = "account.api"

router = SimpleRouter()
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),

    path("login/", LoginView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('roles/', RoleListCreateAPIView.as_view(), name='role-list-create'),
    path('roles/<int:pk>/', RoleRetrieveUpdateDestroyView.as_view(), name='role-detail'),
    path('permissions/', PermissionListCreateAPIView.as_view(), name='permission-list-create'),
    path('permissions/<int:pk>/', PermissionRetrieveUpdateDestroyAPIView.as_view(), name='permission-detail'),
    path('roles/<int:pk>/permissions/', RolePermissionListAPIView.as_view(), name='role-permission-list'),
    path('roles/assign-permissions/', AssignPermissionsToRoleAPIView.as_view(), name='assign-permissions'),
]
