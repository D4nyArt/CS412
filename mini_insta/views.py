# File: views.py
# Author: Daniel Arteaga (d4nyart@bu.edu), 09/24/2025 
# Description: Django views for the Mini Instagram application.
# Contains ListView, DetailView, and CreateView for displaying user profiles,
# posts, and creating new posts.

from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, Post, Photo
from .forms import CreatePostForm, UpdateProfileForm

# Create your views here.

class ProfileListView(ListView):
    """Display a list of all user profiles showing username, 
    display name, and profile image for each user"""

    # Model to query for data
    model = Profile
    
    # Template file to render the response
    template_name = "mini_insta/show_all_profiles.html"
    
    # Context variable name to use in template
    context_object_name = "profiles" 

class ProfileDetailView(DetailView):
    """Displays detailed information for a single user profile"""

    model = Profile
    
    template_name = "mini_insta/show_profile.html"
    
    context_object_name = "profile"

class PostDetailView(DetailView):
    """Display detailed information for a single Post."""

    model = Post
    
    template_name = "mini_insta/show_post.html"
    
    context_object_name = "post"

class CreatePostView(CreateView):
    """Handle the creation of a new post for a profile."""

    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_success_url(self):
        """Provide a URL to redirect to after creating a new Post."""
        post_pk = self.object.pk  # Primary key of the profile from URL
        return reverse('show_post', kwargs={'pk': post_pk})

    def get_context_data(self, **kwargs):
        """Add profile to context for template rendering."""
        context = super().get_context_data(**kwargs)

        # Fetch the Profile object using the pk from URL kwargs
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        return context
    
    def form_valid(self, form):
        """Validate and save the form, associating with profile and creating photo if provided."""
        
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile

        result = super().form_valid(form)
        post = self.object  # The saved post instance
        
        """ # Create a Photo if image_url is provided
        if form.cleaned_data.get('image_url'):
            Photo.objects.create(post=post, image_url=form.cleaned_data['image_url'])"""

        files = self.request.FILES.getlist('image_files')

        if files:
            for file in files:
                Photo.objects.create(post=post, image_file=file)


        return result

class UpdateProfileView(UpdateView):

    model = Profile

    form_class = UpdateProfileForm

    template_name = "mini_insta/update_profile_form.html"

class DeletePostView(DeleteView):

    model = Post

    template_name="mini_insta/delete_post_form.html"

    def get_context_data(self, **kwargs):
        """Add post and profile to context for template rendering."""
        context = super().get_context_data(**kwargs)
        
        # Get the post object (already available as self.object)
        post = self.object
        context['post'] = post
        
        # Get the profile associated with the post
        profile = post.profile
        context['profile'] = profile
        
        return context
    
    def get_success_url(self):
        """Redirect to the profile page of the user whose post was deleted."""
        profile_pk = self.object.profile.pk  # Get the profile pk from the post being deleted
        return reverse('show_profile', kwargs={'pk': profile_pk})




        



