# File: views.py
# Author: Daniel Arteaga (d4nyart@bu.edu), 09/24/2025 
# Description: Django views for the Mini Instagram application.
# Contains ListView, DetailView, CreateView, UpdateView, and DeleteView for displaying user profiles,
# posts, and handling post creation, updates, and deletion functionality.

from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, Post, Photo
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginRequiredMixinMiniInsta(LoginRequiredMixin):

    redirect_field_name = "next"

    def get_login_url(self):
        return reverse("login")

    def get_logged_in_profile(self):
        """Return the Profile associated with the authenticated user, if any."""
        if self.request.user.is_authenticated:
            try:
                return Profile.objects.get(user=self.request.user)
            except Profile.DoesNotExist:
                return None
        return None

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
    """Display detailed information for a single Post"""

    model = Post
    
    template_name = "mini_insta/show_post.html"
    
    context_object_name = "post"

class CreatePostView(LoginRequiredMixinMiniInsta, CreateView):
    """Handle the creation of a new post for the logged-in user's profile"""

    # Form class for post creation - handles caption input
    form_class = CreatePostForm
    
    # Template for rendering the post creation form
    template_name = "mini_insta/create_post_form.html"

    def get_success_url(self):
        """Provide a URL to redirect to after creating a new Post"""
        post_pk = self.object.pk  # Primary key of the created post
        return reverse('show_post', kwargs={'pk': post_pk})

    def get_context_data(self, **kwargs):
        """Add profile to context for template rendering"""
        context = super().get_context_data(**kwargs)

        # Get the profile of the logged-in user
        profile = self.get_logged_in_profile()
        context['profile'] = profile
        return context
    
    def form_valid(self, form):
        """Process valid form submission and create associated photos.
        
        Associates the post with the correct profile and creates Photo objects
        for any uploaded image files.
        """
        
        # Get the profile of the logged-in user to associate with this post
        profile = self.get_logged_in_profile()
        form.instance.profile = profile

        result = super().form_valid(form)
        post = self.object  # The saved post instance
        
        # Handle uploaded image files (create Photo objects for each file)
        files = self.request.FILES.getlist('image_files')

        # If files were uploaded, create Photo objects for each one
        if files:
            for file in files:
                Photo.objects.create(post=post, image_file=file)

        return result

class UpdateProfileView(LoginRequiredMixinMiniInsta, UpdateView):
    """Handle updating profile information for the logged-in user's profile"""

    model = Profile

    form_class = UpdateProfileForm

    template_name = "mini_insta/update_profile_form.html"

    def get_object(self, queryset=None):
        """Return the Profile object for the logged-in user"""
        return Profile.objects.get(user=self.request.user)

class DeletePostView(LoginRequiredMixinMiniInsta, DeleteView):
    """Handle deletion of a specific post.
    
    Provides confirmation page and handles the actual deletion of posts
    along with their associated photos
    """

    model = Post

    template_name = "mini_insta/delete_post_form.html"

    def get_context_data(self, **kwargs):
        """Add post and profile information to template context.
        
        Provides both the post being deleted and its associated profile
        for display in the confirmation template.
        """
        context = super().get_context_data(**kwargs)
        
        # Get the post object
        post = self.object
        context['post'] = post
        
        # Get the profile associated with the post for navigation purposes
        profile = post.profile
        context['profile'] = profile
        
        return context
    
    def get_success_url(self):
        """Redirect to profile page after successful post deletion"""
        # Get the profile pk from the post being deleted
        profile_pk = self.object.profile.pk  
        return reverse('show_profile', kwargs={'pk': profile_pk})
    
class UpdatePostView(LoginRequiredMixinMiniInsta, UpdateView):
    """Handle updating caption text for an existing post.    """

    model = Post
    
    form_class = UpdatePostForm

    template_name = "mini_insta/update_post_form.html"

class ShowFollowersDetailView(DetailView):

    model = Profile
    
    template_name = "mini_insta/show_followers.html"

    context_object_name = "profile"
    
class ShowFollowingDetailView(DetailView):
    
    model = Profile

    template_name = "mini_insta/show_following.html"
    
    context_object_name = "profile"

class PostFeedListView(LoginRequiredMixinMiniInsta, DetailView):
    """Display the post feed for the logged-in user's profile.
    
    Shows all posts from profiles that the logged-in user follows,
    including post details, photos, likes, and comments.
    """
    
    model = Profile
    
    template_name = "mini_insta/show_feed.html"
    
    context_object_name = "profile"
    
    def get_object(self, queryset=None):
        """Return the Profile object for the logged-in user"""
        return Profile.objects.get(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        """Add the post feed to the template context.
        
        Uses the profile's get_post_feed() method to retrieve posts
        from all profiles that this profile follows
        """
        context = super().get_context_data(**kwargs)
        
        # Get the profile whose feed we're showing
        profile = self.object
        
        # Get all posts from profiles that this profile follows
        post_feed = profile.get_post_feed()
                
        context['post_feed'] = post_feed
        return context

class SearchView(LoginRequiredMixinMiniInsta, ListView):
    """Search view to find profiles and posts based on text query
    
    Displays search form when no query is present, and search results
    when a query is provided. Searches both profiles and posts"""

    model = Post  
    template_name = "mini_insta/search_results.html"
    context_object_name = "post_query_result"

    def get(self, request, *args, **kwargs):
        """Handle GET requests; show search form or process search results"""

        if 'search_query' not in request.GET:
            # Get the profile of the logged-in user
            profile = Profile.objects.get(user=request.user)
            return render(request, "mini_insta/search.html", {'profile': profile})

        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        """Return a QuerySet of Posts that match the search query"""

        # Get the search query from GET parameters
        search_query = self.request.GET.get('search_query', '')
    
        if search_query:
            # Search for posts whose caption contains the search query
            post_query_result = Post.objects.filter(caption__icontains=search_query)
            return post_query_result
        else:
            # Return empty QuerySet if no search query provided
            return Post.objects.none()
    
    def get_context_data(self, **kwargs):
        """Add search related data to template context
        Includes the profile, search query, post results, and profile results"""
        context = super().get_context_data(**kwargs)

        # Add the profile of the logged-in user
        profile = Profile.objects.get(user=self.request.user)
        context['profile'] = profile

        # Add the search query if present
        search_query = self.request.GET.get('search_query', '')

        if search_query:
            context['search_query'] = search_query
            context['post_query_result'] = self.get_queryset()
            
            # Search for profiles whose username, display_name or bio_text contains the search query
            profiles_query1 = Profile.objects.filter(username__icontains=search_query)
            profiles_query2 = Profile.objects.filter(display_name__icontains=search_query) 
            profiles_query3 = Profile.objects.filter(bio_text__icontains=search_query)
            
            # Union removes duplicates automatically
            context['profile_query_results'] = profiles_query1.union(profiles_query2, profiles_query3)
        else:
            #Return empty context because query has not been provided
            context['post_query_result'] = Post.objects.none()
            context['profile_query_results'] = Profile.objects.none()
    
        return context
