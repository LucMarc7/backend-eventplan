from django.core.serializers import get_serializer
from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from events.models import Mariage
from invitations.models import Invitation
from invitations.serializers import InvitationDetailSerializer, InvitationValidationSerializer


# Create your views here.

class ControlesInvitationView(ModelViewSet):
    queryset = Invitation.objects.all()
    http_method_names = ['get', 'patch']

    def get_serializer_class(self):
        if self.action == 'patch':
            return InvitationValidationSerializer
        elif self.action == 'retrieve' or self.action == 'list':
            return InvitationDetailSerializer

    def list(self, request, *args, **kwargs):
        """ Liste des invitations """
        try:
            event_code = kwargs.get('event_code')
            organizer_username = kwargs.get('organizer_username')
            if not event_code or not organizer_username:
                return Response({"error": "event_code and organizer_username are required"}, status=status.HTTP_400_BAD_REQUEST)

            mariage = get_object_or_404(Mariage, event_code=event_code)
            if mariage.organizer.username != organizer_username:
                return Response({"error": "Les informations d'accès sont erronées !"}, status=status.HTTP_400_BAD_REQUEST)
        except Mariage.DoesNotExist:
            return Response({"error": "Les informations d'accès sont erronées !"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        invitations = Invitation.objects.filter(event=mariage)

        print("invitations", invitations)
        serializer = self.get_serializer(invitations, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """ Détails d'une invitation """
        try:
            guest_code = kwargs.get('guest_code')
            if not guest_code :
                return Response({"error": "guest_code is required"}, status=status.HTTP_400_BAD_REQUEST)

            invitation = get_object_or_404(Invitation, code_invit=guest_code)

        except Invitation.DoesNotExist:
            return Response({"error": "Cette invitation n'existe pas !"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = self.get_serializer(invitation)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        """ Validation d'une invitation """
        try:
            guest_id = kwargs.get('guest_id')
            if not guest_id :
                return Response({"error": "guest_id is required"}, status=status.HTTP_400_BAD_REQUEST)

            invitation = get_object_or_404(Invitation, id=guest_id)

        except Invitation.DoesNotExist:
            return Response({"error": "Cette invitation n'existe pas !"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = self.get_serializer(invitation, data=request.data, partial=True)


        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.data, status=status.HTTP_200_OK)