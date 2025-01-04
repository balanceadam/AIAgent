"""delivery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.views import serve
from django.urls import path, re_path, include
from drf_yasg2.views import get_schema_view
from drf_yasg2 import openapi
from rest_framework import permissions


def return_static(request, path, insecure=True, **kwargs):
    return serve(request, path, insecure, **kwargs)


schema_view = get_schema_view(openapi.Info(title='Project E API docs', default_version='v1'), public=True, permission_classes=(permissions.IsAdminUser,))


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('account/', include('account.urls')),
    path('assets/', include('assets.urls')),
    path('generic/', include('generic.urls')),
    path('social/', include('social.urls')),
    path('wallet/', include('wallet.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^doc(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
        re_path(r'^static/(?P<path>.*)$', return_static, name='static'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
