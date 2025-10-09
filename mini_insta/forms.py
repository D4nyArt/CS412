# File: forms.py
# Author: Daniel Arteaga (d4nyart@bu.edu), 10/01/2025
# Description: Django forms for the Mini Instagram application.
# Contains the CreatePostForm for creating new posts with captions and optional images.

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    """Form for creating a new post with caption and image URL"""

    #extra URL field for the post's image (No longer required, cause user is now uploading actual img)
    #image_url = forms.URLField(required=False) 
        
    class Meta:
        model = Post 
        fields = ['caption']

class UpdateProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['display_name', 'profile_image_url', 'bio_text']


class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption']    