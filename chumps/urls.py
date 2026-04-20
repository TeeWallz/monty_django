from django.urls import path
from . import views

urlpatterns = [
    path('api/chumps/', views.chumps_api, name='chumps_api'),
    path('api/timeline.json', views.timeline_json, name='timeline_json'),
    path('', views.index, name='index'),
    path('1990/', views.index_1990, name='index_1990'),
    path('1990/entry/', views.entry_1990, name='entry_1990'),
    path('1990/history/', views.history, name='history'),
    path('1990/stats/', views.stats, name='stats'),
    path('1990/cool_pix/', views.cool_pix, name='cool_pix'),
    path('1990/wpaper/', views.wpaper, name='wpaper'),
    path('1990/mycats/', views.mycats, name='mycats'),
]
