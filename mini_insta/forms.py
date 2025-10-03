# File: forms.py
# Author: Daniel Arteaga (d4nyart@bu.edu), 10/01/2025
# Description: Django forms for the Mini Instagram application.
# Contains the CreatePostForm for creating new posts with captions and optional images.

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    """Form for creating a new post with caption and image URL"""
    
    image_url = forms.URLField(required=False)  #extra URL field for the post's image
    
    class Meta:
        model = Post 
        fields = ['caption']
        