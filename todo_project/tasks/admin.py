from django.contrib import admin
from .models import Task, Category, Profile
admin.site.register([Task, Category, Profile])
