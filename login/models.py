from __future__ import unicode_literals
from django.contrib import admin
from django.db import models


class WebUser(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField(null=True)


class CityWeather(models.Model):
    cityname = models.CharField(max_length=20)
    date = models.CharField(max_length=10)
    high = models.CharField(max_length=20)
    low = models.CharField(max_length=10)
    fx = models.CharField(max_length=20)
    fl = models.CharField(max_length=20)
    type = models.CharField(max_length=10)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'email')


admin.site.register(WebUser, UserAdmin)
