from django.db import models
from django.contrib.auth.models import User
import uuid
from invitations.models import Invitation
# Create your models here.


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Event(models.Model):
    """ Event Base class """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    event_image = models.ImageField(upload_to='images/events', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events', null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    heure_debut = models.TimeField(null=True, blank=True)
    heure_fin = models.TimeField(null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    # guests = models.ManyToManyField('invitations.Invitation', related_name='guests', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class Mariage(Event):
    """ Mariage Event """
    event_code = models.CharField(max_length=255, null=True, blank=True)
    mari = models.CharField(max_length=255, null=True, blank=True)
    femme = models.CharField(max_length=255, null=True, blank=True)
    salle = models.CharField(max_length=255, null=True, blank=True)
    ville  = models.CharField(max_length=255, null=True, blank=True)
    avenue = models.CharField(max_length=255, null=True, blank=True)
    commune = models.CharField(max_length=255, null=True, blank=True)
    reference = models.CharField(max_length=255, null=True, blank=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


    class Meta:
        verbose_name = "Mariage"
        verbose_name_plural = "Mariages"
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Conference(Event):
    title = models.CharField(max_length=255, null=True, blank=True)
    total_guest_number = models.IntegerField(default=0)
    ville = models.CharField(max_length=255, null=True, blank=True)
    commune = models.CharField(max_length=255, null=True, blank=True)
    avenue = models.CharField(max_length=255, null=True, blank=True)
    reference = models.CharField(max_length=255, null=True, blank=True)
    place = models.CharField(max_length=100, null=True, blank=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Conference'
        verbose_name_plural = 'Conferences'
        ordering = ['-created_at']

    def __str__(self):
        return self.title



class BirthDay(Event):
    """ Birthday Event """
    birthday_celebrant = models.CharField(max_length=100, null=True, blank=True)
    total_guest_number = models.IntegerField(default=0)
    ville = models.CharField(max_length=255, null=True, blank=True)
    commune = models.CharField(max_length=255, null=True, blank=True)
    avenue = models.CharField(max_length=255, null=True, blank=True)
    reference = models.CharField(max_length=255, null=True, blank=True)
    place = models.CharField(max_length=100, null=True, blank=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Anniversaire'
        verbose_name_plural = 'Anniversaires'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class Concert(Event):
    """ Concert Event """
    theme_concert = models.CharField(max_length=100, null=True, blank=True)
    artist = models.CharField(max_length=255, null=True, blank=True)
    total_ticket_number = models.IntegerField(default=0)
    ville = models.CharField(max_length=100, null=True, blank=True)
    commune = models.CharField(max_length=100, null=True, blank=True)
    avenue = models.CharField(max_length=100, null=True, blank=True)
    reference = models.CharField(max_length=100, null=True, blank=True)
    place = models.CharField(max_length=100, null=True, blank=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Concert'
        verbose_name_plural = 'Concerts'
        ordering = ['-created_at']

    def __str__(self):
        return self.name