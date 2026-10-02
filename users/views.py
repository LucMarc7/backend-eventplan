from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import (
    RegisterSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    AvatarUploadSerializer,
    LoginSerializer,
)
from .models import UserProfile

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

# Imports pour désactiver CSRF
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


# ==================== VUES EXISTANTES (INCHANGÉES) ====================

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"detail": "Username and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=username, password=password)

        if user is not None:
            user_infos = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "user": user_infos,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"detail": "Invalid credentials !"}, status=status.HTTP_401_UNAUTHORIZED
        )


@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    """
    Contrainte:
        data : 'refresh_token'
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, **kwargs):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            logout(request)
            return Response(
                {"detail": "Successfully logged out."}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST
            )


@method_decorator(csrf_exempt, name='dispatch')
class RegisterViewSet(viewsets.ModelViewSet):
    """
    Create a new user in the system

    returns:
        {
            "user": {
                "id": xx,
                "username": "xxx",
                "email": "example@mail.com",
                "first_name": "xxx",
                "last_name": "xxx"
            },
            "refresh": "RefreshToken",
            "access": "AccessToken",
        }
    """

    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    http_method_names = ["post"]

    @action(detail=False, methods=["post"])
    def register(self, request):
        """
        Créer un nouvel utilisateur.
        """
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                    },
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    Get profile

    returns:
        profile: object
        roles : [collection]
    """

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def detail_profile(self, request):
        """
        Renvoie uniquement le profil de l'utilisateur connecté et ses roles.
        """
        user = request.user
        if user.is_authenticated:
            roles = user.groups.values_list("name", flat=True)
            profile = UserProfile.objects.get(user=user)
            serializer = self.get_serializer(profile)
            return Response(
                {"profile": serializer.data, "roles": roles}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED
            )

    @action(detail=False, methods=["post"])
    def update_profile(self, request):
        """
        Met à jour le profil de l'utilisateur connecté.
        """
        profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordViewSet(viewsets.ModelViewSet):
    """
    Change password

    parameters:
        old_password: string
        new_password: string
        confirm_password: string

    returns:
        detail: string
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    http_method_names = ["post"]

    @action(detail=False, methods=["post"])
    def change_password(self, request):
        """
        Met à jour le mot de passe de l'utilisateur connecté.
        """
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Mot de passe modifié avec succès."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetRequestView(APIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Email envoyé avec un lien de réinitialisation."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetConfirmView(APIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, uid, token):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(uid=uid, token=token)
            return Response(
                {"message": "Mot de passe mis à jour avec succès."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ================== NOUVELLES VUES POUR LE PROFIL (AJOUT) ==================

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Vue pour récupérer (GET) et mettre à jour (PATCH) le profil utilisateur.
    Correspond à l'endpoint /auth/profile/me/
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Récupère le profil de l'utilisateur connecté
        return self.request.user.profile


class AvatarUploadView(APIView):
    """
    Vue pour uploader (POST) et supprimer (DELETE) l'avatar.
    Correspond à l'endpoint /auth/profile/avatar/
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = AvatarUploadSerializer(data=request.data)
        if serializer.is_valid():
            avatar = serializer.validated_data['avatar']
            profile = request.user.profile
            profile.profile_image = avatar
            profile.save()
            return Response({'avatar': profile.profile_image.url}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        profile = request.user.profile
        if profile.profile_image:
            profile.profile_image.delete(save=True)
            return Response({'detail': 'Avatar supprimé avec succès'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Aucun avatar à supprimer'}, status=status.HTTP_400_BAD_REQUEST)