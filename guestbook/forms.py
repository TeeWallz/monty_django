from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from captcha.fields import CaptchaField
from .models import Entry


class EntryForm(forms.ModelForm):
    captcha = CaptchaField()
    location = CountryField(blank=True).formfield(
        blank_label="(Select country)",
        widget=CountrySelectWidget(),
    )

    class Meta:
        model = Entry
        fields = ("name", "email", "location", "message", "captcha")
