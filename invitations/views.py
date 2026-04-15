import os
from rest_framework import status, viewsets
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from .models import Invitation
from events.models import Event
from .serializers import InvitationSerializer, InvitationDetailSerializer
from .utils import generate_code_invit, qr_code_generator
# Create your views here.

class InvitationViewSet(viewsets.ModelViewSet):
    """
    Vue Invitation - Gestion des invitations par un Organisateur.
    """
    queryset = Invitation.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'list' or self.action == 'update':
            return InvitationSerializer
        elif self.action == 'retrieve':
            return InvitationDetailSerializer
        return InvitationSerializer

    def list(self, request, *args, **kwargs):
        """ Création d'une invitation : L'ID de l'évènement 'event_id' est requis pour le filtre   """
        try:
            event_id = kwargs.get('event_id')
            if event_id:
                event = get_object_or_404(Event, pk=event_id)
            else:
                return Response({"error": "event_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"error": "event_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Invitation.objects.filter(event=event)
        serializer = InvitationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """ Création d'une invitation : L'ID de l'évènement 'event_id' est requis pour association   """
        try:
            event_id = kwargs.get('event_id')
            if not event_id:
                return Response({"error": "event_id is required"}, status=status.HTTP_400_BAD_REQUEST)
            event = get_object_or_404(Event, pk=event_id)
        except Exception:
            return Response({"error": "event_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        code = generate_code_invit()
        data = request.data.copy() # Récupération des données

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            event.save()
            invitation = serializer.instance
            invitation.code_invit = code # Ajout du code l'invitation
            invitation.event = event
            invitation.qr_code = qr_code_generator(data=code) # Ajout de l'image du code QR à l'invitation

            # Créer le dossier de destination pour le QR code s'il n'existe pas
            qr_dir = os.path.join(settings.MEDIA_ROOT, 'images', 'qr_code')
            os.makedirs(qr_dir, exist_ok=True)

            invitation.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """ Détails d'une invitation : L'ID de l'invitation est requis 'invitation_id' """
        try:
            invitation_id = kwargs.get('invitation_id')
            if not invitation_id:
                return Response({"error": "invitation_id is required"}, status=status.HTTP_400_BAD_REQUEST)
            invitation = get_object_or_404(Invitation, pk=invitation_id)
        except Exception:
            return Response({"error": "invitation_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(invitation)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """ Modification d'une invitation : L'ID de l'invitation est requis 'invitation_id' """
        try:
            invitation_id = kwargs.get('invitation_id')
            if not invitation_id:
                return Response({"error": "invitation_id is required"}, status=status.HTTP_400_BAD_REQUEST)
            invitation = get_object_or_404(Invitation, pk=invitation_id)
        except Exception:
            return Response({"error": "invitation_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(invitation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """ Suppression d'une invitation : L'ID de l'invitation est requis 'invitation_id' """
        try:
            invitation_id = kwargs.get('invitation_id')
            if not invitation_id:
                return Response({"error": "invitation_id is required"}, status=status.HTTP_400_BAD_REQUEST)
            invitation = get_object_or_404(Invitation, pk=invitation_id)
        except Exception:
            return Response({"error": "L'invitation indiqué n'existe pas"}, status=status.HTTP_400_BAD_REQUEST)

        invitation.delete()
        return Response({"message": "Deleted successfuly"}, status=status.HTTP_204_NO_CONTENT)