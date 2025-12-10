# File: apps.py
# Author: Daniel Arteaga (d4nyart@bu.edu), 12/9/2025
# Description: App configuration for the project application.

from django.apps import AppConfig


class ProjectConfig(AppConfig):
    """
    Configuration class for the project application.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "project"
