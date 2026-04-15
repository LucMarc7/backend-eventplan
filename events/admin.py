from django.contrib import admin
from .models import Event, Category, Mariage, Concert, BirthDay, Conference
# Register your models here.

admin.site.register(Event)
admin.site.register(Mariage)
admin.site.register(Category)
admin.site.register(Concert)
admin.site.register(BirthDay)
admin.site.register(Conference)

