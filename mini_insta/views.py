# File: views.py
# Author: Daniel Arteaga (d4nyart@bu.edu), 09/24/2025 
# Description: Django views for the Mini Instagram application.
# Contains ListView and DetailView for displaying user profiles
# in both list and individual detail formats.

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile, Post
from .forms import CreatePostForm

# Create your views here.

class ProfileListView(ListView):
    """Display a list of all user profiles.
    
    This view renders all Profile objects in a grid layout,
    showing username, display name, and profile image for each user.
    Users can click on any profile to view detailed information.
    """
    # Model to query for data
    model = Profile
    
    # Template file to render the response
    template_name = "mini_insta/show_all_profiles.html"
    
    # Context variable name to use in template
    context_object_name = "profiles" 

class ProfileDetailView(DetailView):
    """Display detailed information for a single user profile.
    
    This view shows all the information of the current profile 
    that is being displayed.
    """
    # Model to query for data
    model = Profile
    
    # Template file to render the response
    template_name = "mini_insta/show_profile.html"
    
    # Context variable name to use in template
    context_object_name = "profile"

class PostDetailView(DetailView):
    """Display detailed information for a single Post """
    # Model to query for data
    model = Post
    
    # Template file to render the response
    template_name = "mini_insta/show_post.html"
    
    # Context variable name to use in template
    context_object_name = "post"

class CreatePostView(CreateView):

    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"
    
