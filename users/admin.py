from django.contrib import admin
from .models import UserProfile
from django.utils.translation import gettext_lazy as _
# Register your models here.


admin.site.register(UserProfile)

admin.site.site_header = _('EVENT PLAN ADMIN')

