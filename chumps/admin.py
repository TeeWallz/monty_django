from django.contrib import admin

from .models import Chump, ChumpMedia, SpecialEvent, Era

admin.site.register(Chump)
admin.site.register(ChumpMedia)
admin.site.register(SpecialEvent)
admin.site.register(Era)
