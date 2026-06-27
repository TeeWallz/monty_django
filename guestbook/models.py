from django.db import models
from django_countries.fields import CountryField


class Entry(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    location = CountryField(blank=True)
    message = models.TextField()
    published = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Entries"
