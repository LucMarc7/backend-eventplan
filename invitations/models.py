import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Invitation(models.Model):
    """ Modèle des invitations """
    INVITATION_TYPES = (
        ("COUPLE", "COUPLE"),
        ("SINGLETON", "SINGLETON")
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey("events.Event", verbose_name=_("Événement"), related_name="invitations", on_delete=models.CASCADE, null=True, blank=True)
    code_invit = models.CharField(_("Code d'invitation"), max_length=50, null=True, blank=True)
    invitation_type = models.CharField(_("Type d'invitation"), max_length=50, choices=INVITATION_TYPES, default="SINGLETON")
    qr_code = models.ImageField(_("Code QR"), upload_to="images/qr_code", blank=True)
    first_person = models.CharField(_("Première personne"), max_length=50, null=True, blank=True)
    second_person = models.CharField(_("Deuxième personne"), max_length=50, null=True, blank=True)
    place = models.CharField(_("Place"), max_length=50, null=True, blank=True)
    email = models.EmailField(_("Email"), max_length=50, null=True, blank=True)
    tel = models.CharField(_("Téléphone"), max_length=50, null=True, blank=True)
    used = models.BooleanField(_("Utilisé"), default=False)
    created_date = models.DateTimeField(_("Date de création"), auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name = _("Invitation")
        verbose_name_plural = _("Invitations")
        ordering = ['-created_date']


    def __str__(self) -> str:
        return f"invitation {self.first_person}"