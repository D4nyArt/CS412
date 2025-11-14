
# File: serializers.py
# Author: Daniel Arteaga (d4nyart@bu.edu), 11/14/2025
# Description: Django REST Framework serializers for the 
# dadjokes web application.

from rest_framework import serializers
from .models import Joke, Picture


class JokeSerializer(serializers.ModelSerializer):
    """Serializer for the Joke model"""
    
    class Meta:
        model = Joke
        fields = ['id', 'text', 'contributor', 'timestamp']
        read_only_fields = ['id', 'timestamp']


class PictureSerializer(serializers.ModelSerializer):
    """Serializer for the Picture model"""
    
    class Meta:
        model = Picture
        fields = ['id', 'image_url', 'contriubutor', 'timestamp']
        read_only_fields = ['id', 'timestamp']
