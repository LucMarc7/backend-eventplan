from django.urls import path, include
from . import views

urlpatterns = [
    path('api/create_invitation/<event_id>/', views.InvitationViewSet.as_view({'post': 'create'}), name='invitation-create' ),
    path('api/invitations_list/<event_id>/', views.InvitationViewSet.as_view({'get': 'list'}), name='invitation-list-by-event'),
    path('api/retrieve_invitation/<invitation_id>/', views.InvitationViewSet.as_view({'get': 'retrieve'}), name='invitation-retrieve'),
    path('api/update_invitation/<invitation_id>/', views.InvitationViewSet.as_view({'put': 'update'}), name='invitation-update'),
    path('api/delete_invitation/<invitation_id>/', views.InvitationViewSet.as_view({'delete': 'destroy'}), name='invitation-destroy'),
]