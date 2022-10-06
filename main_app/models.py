from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Parks(models.Model):

    name = models.CharField(max_length=150)
    img = models.CharField(max_length=500)
    bio = models.TextField(max_length=1000)
    verified_park = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Site(models.Model):

    title = models.CharField(max_length=150)
    parks = models.ForeignKey(Parks, on_delete=models.CASCADE, related_name="sites")

    def __str__(self):
        return self.title


# Playlist model
class Favoritelist(models.Model):

    title = models.CharField(max_length=150)
    # this is many-to-many field, this will create our join table
    sites = models.ManyToManyField(Site)

    def __str__(self):
        return self.title