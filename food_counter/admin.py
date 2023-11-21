from django.contrib import admin
from .models import Meal, Date, Category, Products

# Register your models here.
admin.site.register(Meal)
admin.site.register(Date)
admin.site.register(Products)
admin.site.register(Category)

