# File: admin.py
# Author: Daniel Arteaga (d4nyart@bu.edu), 09/24/2025 
# Description: Django admin configuration for the Mini Instagram application.
# Registers the Profile model with Django's admin interface to allow
# administrators to view, create, edit, and delete user profiles.

from django.contrib import admin

# Register your models here.
from .models import Profile

# Register the Profile model with the admin site
admin.site.register(Profile)
