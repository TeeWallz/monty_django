from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index_view"),
    path("sign/", views.sign, name="sign_view"),
]
