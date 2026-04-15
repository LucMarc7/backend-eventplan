from django.urls import path
from . import views

urlpatterns = [
    # Liste des mariages (GET) et création (POST)
    path('api/mariages/', views.MariageListView.as_view(), name='mariage-list'),
    # Détail d'un mariage (GET, PUT, PATCH, DELETE)
    path('api/mariages/<int:pk>/', views.MariageDetailView.as_view(), name='mariage-detail'),
]