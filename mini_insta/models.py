# File: models.py
# Author: Daniel Arteaga (d4nyart@bu.edu), 09/24/2025 
# Description: Django models for the Mini Instagram application.
# Contains the Profile model that represents user profiles with
# username, display name, profile image, bio, and join date.

from django.db import models

# Create your models here.


class Profile(models.Model): 
    """Encapsulate the data of a Profile of a person.
    
    This model represents a user profile in our Mini Instagram application,
    storing information about each user including their username,
    display name, profile image URL, biographical text, and join date.
    """
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    # URL pointing to the user's profile image
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)    
    # Automatically set to current date/time when profile is created
    join_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return string representation of the profile."""
        return f"{self.username}"
