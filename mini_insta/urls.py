# File: urls.py
# Author: Daniel Arteaga (d4nyart@bu.edu), 09/24/2025 
# Description: URL configuration for the Mini Instagram application.
# Maps URL patterns to their corresponding views for displaying
# user profiles in both list and individual detail formats.

from django.urls import path
from .views import *

# URL patterns for the mini_insta application
urlpatterns = [
    # Root path that displays all profiles in a grid layout
    # Maps to ProfileListView which shows all user profiles
    path(r'', ProfileListView.as_view(), name='show_all_profiles'),
    
    # Profile detail path that displays individual profile information
    # Takes an integer primary key (pk) parameter to identify which profile to show
    # Maps to ProfileDetailView which shows detailed profile information
    path(r'profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile"),

    path(r'post/<int:pk>', PostDetailView.as_view(), name="show_post"),

    path(r'post/create', CreatePostView.as_view(), name="create_post")
]