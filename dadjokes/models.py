from django.db import models

# Create your models here.

class Joke(models.Model):

    text = models.TextField(blank=True)

    contributor = models.TextField(blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return string representation of the like"""
        return f"{self.text}"
    
class Picture(models.Model):

    image_url = models.URLField(blank=True)

    contriubutor = models.TextField(blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} image"
