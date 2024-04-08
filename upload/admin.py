from django.contrib import admin
from django import forms
from .models import Photo


class PhotoForm(forms.ModelForm):
    image = forms.ImageField(label='Upload Image')

    class Meta:
        model = Photo
        fields = ['image']


class PhotoAdmin(admin.ModelAdmin):
    form = PhotoForm


admin.site.register(Photo, PhotoAdmin)
