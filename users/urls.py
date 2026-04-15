from django.urls import path, include
from . import views

from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    # Aunthentication urls
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterViewSet.as_view({'post': 'register'}), name='register'),

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # User Profile urls
    path('profile/', views.UserProfileViewSet.as_view({'get' : 'detail_profile'}), name='profile'),
    path('update/profile/', views.UserProfileViewSet.as_view({'post': 'update_profile'}), name='update_user_profile'),

    # Password manager routes
    path('change_password/', views.ChangePasswordViewSet.as_view({'post':'change_password'}), name='change_password'),
    path('forgot_password/', views.PasswordResetRequestView.as_view(), name='forgot_password'),
    path('reset-password/<uid>/<token>/', views.PasswordResetConfirmView.as_view(), name='confirm_reset_password'),

]