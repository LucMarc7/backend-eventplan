from django.urls import path
from . import views

urlpatterns = [
    path('api/list_invitations/<event_code>/<organizer_username>/', views.ControlesInvitationView.as_view({'get': 'list'}), name='list_invitations'),
    path('api/details_invitation/<guest_code>/', views.ControlesInvitationView.as_view({'get': 'retrieve'}), name='details_invitation'),
    path('api/validation_invitation/<guest_id>/', views.ControlesInvitationView.as_view({'patch': 'patch'}), name='validation_invitations'),

]