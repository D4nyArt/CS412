# File: views.py
# Author: Daniel Arteaga (d4nyart@bu.edu), 09/24/2025 
# Description: Django views for the Mini Instagram application.
# Contains ListView and DetailView for displaying user profiles
# in both list and individual detail formats.

from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile, Post, Photo
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

    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new Post.'''

        pk = self.kwargs['pk']
        return reverse('show_profile', kwargs={'pk':pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch the Profile object using the pk from URL kwargs
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        return context
    
    
    def form_valid(self, form):
        
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile

        result = super().form_valid(form)
        post = self.object  # The saved post instance

        # Create a Photo if image_url is provided
        if form.cleaned_data.get('image_url'):
            Photo.objects.create(post=post, image_url=form.cleaned_data['image_url'])

        return result

        



