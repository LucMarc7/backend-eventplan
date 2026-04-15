from rest_framework import serializers
from .models import Invitation

class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        exclude = ('qr_code', "code_invit",'used', 'event', 'created_date')
        read_only_fields = ('id',)


class InvitationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        exclude = ('event',)
        read_only_fields = ('id',)


class InvitationValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['used']
        read_only_fields = ('id',)