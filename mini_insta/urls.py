# File: urls.py
# Author: Daniel Arteaga (d4nyart@bu.edu), 09/24/2025 
# Description: URL configuration for the Mini Instagram application.
# Maps URL patterns to their corresponding views for displaying
# user profiles, posts, and creating new posts.

from django.urls import path
from .views import *

# URL patterns for the mini_insta application
urlpatterns = [
    
    # Root path that displays all profiles in a grid layout
    path(r'', ProfileListView.as_view(), name='show_all_profiles'),
    
    # Profile detail path that displays individual profile information
    # Takes an integer primary key (pk) parameter to identify which profile to show
    path(r'profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile"),

    # Post detail path that displays individual post information
    # Takes an integer primary key (pk) parameter to identify which post to show
    path(r'post/<int:pk>', PostDetailView.as_view(), name="show_post"),

    # Create post path for a specific profile
    # Takes an integer primary key (pk) parameter for the profile
    path(r'profile/<int:pk>/create_post', CreatePostView.as_view(), name="create_post"),

    path(r'profile/<int:pk>/update_profile', UpdateProfileView.as_view(), name="update_profile"),

    # Delete post path for a specific post
    # Takes an integer primary key (pk) parameter for the post to delete
    path(r'post/<int:pk>/delete', DeletePostView.as_view(), name="delete_post")
]