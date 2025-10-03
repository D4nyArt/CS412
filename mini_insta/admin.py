# File: admin.py
# Author: Daniel Arteaga (d4nyart@bu.edu), 09/24/2025 
# Description: Django admin configuration for the Mini Instagram application.
# Registers the Profile, Post, and Photo models with Django's admin interface to allow
# administrators to view, create, edit, and delete these objects.

from django.contrib import admin

# Register your models here.
from .models import Profile, Post, Photo

# Registration of models for admin management
admin.site.register(Profile)  
admin.site.register(Post)  
admin.site.register(Photo) 

