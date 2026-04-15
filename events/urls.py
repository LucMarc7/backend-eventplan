from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('category_events', views.EventCategoryViewSet, basename='category_events')
router.register('mariages', views.MariageViewSet, basename='mariages')
router.register('birthdays', views.BirthDayViewSet, basename='birthdays')
router.register('concerts', views.ConcertViewset, basename='concerts')
router.register('events', views.ConferenceViewSet, basename='conferences')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/ajout/image/<uuid:event_id>/', views.MariageViewSet.as_view({'patch':'patch'}), name='ajout-image'),
    path('ping/', views.ping, name='ping'),
]