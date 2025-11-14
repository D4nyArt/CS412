
# File: models.py
# Author: Daniel Arteaga (d4nyart@bu.edu), 11/14/2025
# Description: Django models for the dadjokes web application, 
# including Joke and Picture models.

from django.db import models

class Joke(models.Model):

    text = models.TextField(blank=True)

    contributor = models.TextField(blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return string representation of the joke"""
        return f"{self.text}"
    
class Picture(models.Model):

    image_url = models.URLField(blank=True)

    contriubutor = models.TextField(blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return string representation of the joke"""
        return f"{self.id} image"
