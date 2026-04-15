from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import generate_code_username
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes



class UserSerializer(serializers.ModelSerializer):
    """ Serializer for user model """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError('User account is disabled.')
                return user
            else:
                raise serializers.ValidationError('Unable to log in with provided credentials.')
        else:
            raise serializers.ValidationError('Must include "username" and "password".')


    def create(self, validated_data):
        user = validated_data
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['country', 'city', 'address']


class RegisterSerializer(serializers.ModelSerializer):
    """ Serializer to register a new user """
    userprofile = ProfileSerializer()
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name','password', 'password2','userprofile')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        username = validated_data.get('username')
        username = generate_code_username(username)
        user = User.objects.create(
            username=username,
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        profile = UserProfile.objects.get(user=user)
        profile.country = validated_data.get('userprofile')["country"]
        profile.city = validated_data.get('userprofile')["city"]
        profile.address = validated_data.get('userprofile')["address"]
        profile.save()

        return user

class ChangePasswordSerializer(serializers.Serializer):
    """ Serializer to change user password """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        if not user.check_password(self.validated_data['old_password']):
            raise serializers.ValidationError("L'ancien mot de passe est incorrect.")
        user.set_password(self.validated_data['new_password'])
        user.save()
        self.context['request'].session.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """ Serializer to get user profile"""
    class Meta:
        model = UserProfile
        exclude = ['user']


class PasswordResetRequestSerializer(serializers.Serializer):
    """ Serializer de la demande de réinitialisation du password """
    email = serializers.EmailField()

    def validate_email(self, value):
        """ Vérifie si l'email existe dans la base de données """
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Aucun compte associé à cet email.")
        return value

    def save(self):
        """ Génère un token et envoie un e-mail """
        email = self.validated_data["email"]
        user = User.objects.get(email=email)

        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_link = f"masma.pythonanywhere.com/accounts/reset-password/{uid}/{token}/"


        user.email_user(
            "Réinitialisation de votre mot de passe",
            f"Bonjour, \n\nCliquez sur le lien ci-dessous pour réinitialiser votre mot de passe :\n{reset_link}\n\nSi vous n'avez pas demandé ce changement, ignorez cet email."
        )
        return reset_link


class PasswordResetConfirmSerializer(serializers.Serializer):
    """ Serializer de la confirmation de la modification du mot de passe """
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return data

    def save(self, uid, token):
        """ Vérifie le token et met à jour le mot de passe """
        try:
            user_id = force_bytes(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Lien invalide ou expiré.")

        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            raise serializers.ValidationError("Lien de réinitialisation invalide ou expiré.")


        user.set_password(self.validated_data["new_password"])
        user.save()
        return user