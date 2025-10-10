# File: forms.py
# Author: Daniel Arteaga (d4nyart@bu.edu), 10/01/2025
# Description: Django forms for the Mini Instagram application.
# Contains forms for creating and updating posts and profiles, including
# caption input and profile information updates.

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    """Form for creating a new post"""
    class Meta:
        # Model this form is based on
        model = Post 
        # Fields to include in the form
        fields = ['caption']

class UpdateProfileForm(forms.ModelForm):
    """Form for updating user profile information"""
    class Meta:
        model = Profile
        fields = ['display_name', 'profile_image_url', 'bio_text']


class UpdatePostForm(forms.ModelForm):
    """Form for updating existing post caption text"""
    class Meta:
        model = Post
        fields = ['caption']    