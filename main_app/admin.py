from django.contrib import admin
from .models import Favoritelist, Parks, Site

# Register your models here.
admin.site.register(Parks)
admin.site.register(Site)
admin.site.register(Favoritelist)