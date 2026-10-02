"""
URL configuration for eventplan_core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



schema_view = get_schema_view(
   openapi.Info(
       title="Plan Event API",
       default_version='v1',
       description="Api d'une application de gestion des événements.",
       terms_of_service="https://",
       contact=openapi.Contact(email="jephtedunia07@gmail.com"),
       #license=openapi.License(name="BSD License"),
   ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('events/', include('events.urls')),
    path('invitations/', include('invitations.urls')),
    path('controles/', include('controles.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/', include('users.urls')),   # ← conserve la ligne existante

    # ========== AJOUT POUR LE PROFIL (sous /auth/) ==========
    # Permet d'accéder aux mêmes endpoints via /auth/ (plus cohérent avec le frontend)
    path('auth/', include('users.urls')),

    # Docs Route
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)