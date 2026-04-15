from django.http import JsonResponse

def ping(request):
    return JsonResponse({"ping": "pong"})

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from invitations.models import Invitation
from .models import Mariage, Category, Event, BirthDay, Concert
from .serializers import MariageSerializer, EventCategorySerializer, EventImageSerializer, BirthDaySerializer, ConcertSerializer, ConferenceSerializer
from .utils import generate_mariage_code

# Create your views here.


class EventCategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = EventCategorySerializer
    http_method_names = ['get']


    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter()
        serializer = EventCategorySerializer(queryset, many=True)
        return Response(serializer.data)


# Mariage View
class MariageViewSet(viewsets.ModelViewSet):
    """
    Vue Mariage
    *Endpoints de la gestion d'un événement de catégorie 'Mariage'

    Context :
        * L'Utilisateur doit être connecté (Organisateur)

    """
    queryset = Mariage.objects.all()
    #permission_classes = [IsAuthenticated]
    #authentication_classes = [JWTAuthentication]

    def get_serializer_class(self):
        if self.action == 'patch':
            return EventImageSerializer
        else :
            return MariageSerializer

    def list(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return Response({"error": "You are not authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            organizer = self.request.user
        queryset = self.queryset.filter(organizer=organizer)
        serializer = MariageSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            return Response({"error": "You are not authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            serializer.save(organizer=self.request.user, event_code=generate_mariage_code())


    def patch(self, request, *args, **kwargs):
        try:
            event_id = self.kwargs['event_id']

            if not event_id:
                return Response({"error": "Event id is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            event = get_object_or_404(Event, pk=event_id)

        except event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(event, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# BirthDay View

class BirthDayViewSet(viewsets.ModelViewSet):
    """
    Vue Birthday
    *Endpoints de la gestion d'un événement de catégorie 'Mariage'

    Context :
        * L'Utilisateur doit être connecté (Organisateur)

    """
    queryset = BirthDay.objects.all()
    #permission_classes = [IsAuthenticated]
    #authentication_classes = [JWTAuthentication]

    def get_serializer_class(self):
        if self.action == 'patch':
            return EventImageSerializer
        else :
            return BirthDaySerializer

    def list(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return Response({"error": "You are not authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            organizer = self.request.user
        queryset = self.queryset.filter(organizer=organizer)
        serializer = BirthDaySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            return Response({"error": "You are not authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            serializer.save(organizer=self.request.user, event_code=generate_mariage_code())


    def patch(self, request, *args, **kwargs):
        try:
            event_id = self.kwargs['event_id']

            if not event_id:
                return Response({"error": "Event id is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            event = get_object_or_404(Event, pk=event_id)

        except event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(event, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Concert View

class ConcertViewset(viewsets.ModelViewSet):
    """
    Vue Concert
    *Endpoints de la gestion d'un événement de catégorie 'Mariage'

    Context :
        * L'Utilisateur doit être connecté (Organisateur)

    """
    queryset = Concert.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_serializer_class(self):
        if self.action == 'patch':
            return EventImageSerializer
        else :
            return ConcertSerializer

    def list(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return Response({"error": "You are not authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            organizer = self.request.user
        queryset = self.queryset.filter(organizer=organizer)
        serializer = ConcertSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            return Response({"error": "You are not authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            serializer.save(organizer=self.request.user, event_code=generate_mariage_code())


    def patch(self, request, *args, **kwargs):
        try:
            event_id = self.kwargs['event_id']

            if not event_id:
                return Response({"error": "Event id is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            event = get_object_or_404(Event, pk=event_id)

        except event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(event, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Conference View

class ConferenceViewSet(viewsets.ModelViewSet):
    """
    Vue Mariage
    *Endpoints de la gestion d'un événement de catégorie 'Mariage'

    Context :
        * L'Utilisateur doit être connecté (Organisateur)

    """
    queryset = Mariage.objects.all()

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_serializer_class(self):
        if self.action == 'patch':
            return EventImageSerializer
        else:
            return ConferenceSerializer

    def list(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return Response({"error": "You are not authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            organizer = self.request.user
        queryset = self.queryset.filter(organizer=organizer)
        serializer = ConferenceSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            return Response({"error": "You are not authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            serializer.save(organizer=self.request.user, event_code=generate_mariage_code())

    def patch(self, request, *args, **kwargs):
        try:
            event_id = self.kwargs['event_id']

            if not event_id:
                return Response({"error": "Event id is required"}, status=status.HTTP_400_BAD_REQUEST)

            event = get_object_or_404(Event, pk=event_id)

        except event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(event, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)