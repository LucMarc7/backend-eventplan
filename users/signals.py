from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Création du profile associé à l'utilisateur

        profile = UserProfile.objects.create(user=instance)
        profile.username = instance.username
        profile.email = instance.email
        profile.first_name = instance.first_name
        profile.last_name = instance.last_name
        profile.save()

        # Ajout ou creation du groupe
        client_group, created = Group.objects.get_or_create(name='ORGANISATEUR')
        instance.groups.add(client_group)


@receiver(post_save, sender=UserProfile)
def update_user_profile(sender, instance, **kwargs):
    if not kwargs.get('update_fields', None):
        if instance.first_name:
            instance.user.first_name = instance.first_name
        if instance.last_name:
            instance.user.last_name = instance.last_name
        if instance.email:
            instance.user.email = instance.email
        instance.user.save(update_fields=['first_name', 'last_name', 'email'])