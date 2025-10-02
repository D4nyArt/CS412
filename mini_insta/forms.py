from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    
    image_url = forms.URLField(required=False)
    
    class Meta:
        model = Post 
        fields = ['caption']
        