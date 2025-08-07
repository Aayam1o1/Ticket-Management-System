"""Defines URL patterns for the APIs, documentation."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions

urlpatterns = []
api_urls = [
    
]

web_urls = [
    path("admin/", admin.site.urls),
]


urlpatterns += [
    path("api/v1/", include(api_urls)),
    path("", include(web_urls)),
]

if settings.DEBUG:
    import debug_toolbar
    from drf_yasg import openapi
    from drf_yasg.views import get_schema_view

    schema_view = get_schema_view(
        openapi.Info(
            title="EIA API",
            default_version="v1",
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

    dev_urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
        path(
            "swagger/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
    ]
    urlpatterns += dev_urlpatterns
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
