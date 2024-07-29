from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *
from django.db.models import Sum

admin.site.register(Receipt)
