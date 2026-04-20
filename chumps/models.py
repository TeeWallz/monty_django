from django.db import models
from django.utils.text import slugify
import datetime

class Chump(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    date = models.DateField()
    date_order = models.IntegerField(default=0)
    thanks = models.CharField(max_length=255, default="")
    url = models.URLField(max_length=255, default="")
    

    def __str__(self):
        return self.name

    def __pojo__(self):
        return {
            'name': self.name,
            'slug': self.slug,
            'date': self.date,
            'date_order': self.date_order,
            'thanks': self.thanks,
            'localised_date': self.date.strftime('%d %B %Y'),
            'url': self.url,
            'media': [media.__pojo__() for media in self.media.all().order_by('media_order')],
        }

class ChumpMedia(models.Model):
    chump = models.ForeignKey(Chump, on_delete=models.CASCADE, related_name='media')
    media_type = models.CharField(max_length=50)
    media = models.ImageField(upload_to='chumps/')
    media_order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.chump.name} - {self.media_type}"

    def __pojo__(self, include_chump=False):
        media = {
            'media_type': self.media_type,
            'url': self.media.url,
            'media_order': self.media_order,
        }
        if include_chump:
            media['chump'] = self.chump.__pojo__()
        return media

class Era(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    text = models.TextField(max_length=255, default="")

    def __str__(self):
        return self.name

    def __pojo__(self):
        return {
            'name': self.name,
            'start_date': self.start_date,
            'end_date': self.end_date if self.end_date else datetime.date.today(),
            'text': self.text,
        }

    def __lib_pojo__(self):
        return {
            'start_date': {
                'year': self.start_date.year,
                'month': self.start_date.month
            },
            'end_date': {
                'year': self.end_date.year if self.end_date else datetime.date.today().year,
                'month': self.end_date.month if self.end_date else datetime.date.today().month
            },
            'text': {
                'headline': self.name,
                'text': self.text
            }
        }

class SpecialEvent(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    text = models.CharField(max_length=255, default="")
    background_color = models.CharField(max_length=7, default="#4a6da7")

    def __str__(self):
        return self.name

    def __pojo__(self):
        return {
            'name': self.name,
            'date': self.date,
            'text': self.text,
            'background_color': self.background_color,
        }