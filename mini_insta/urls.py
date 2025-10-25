# File: urls.py
# Author: Daniel Arteaga (d4nyart@bu.edu), 09/24/2025 
# Description: URL configuration for the Mini Instagram application.
# Maps URL patterns to their corresponding views for displaying
# user profiles, posts, and creating new posts.

from django.urls import path
from .views import *

from django.contrib.auth import views as auth_views

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

    # Create post path for the logged-in user's profile
    path(r'profile/create_post', CreatePostView.as_view(), name="create_post"),

    # Update profile path for the logged-in user
    path(r'profile/update', UpdateProfileView.as_view(), name="update_profile"),

    # Delete post path for a specific post
    # Takes an integer primary key (pk) parameter for the post to delete
    path(r'post/<int:pk>/delete', DeletePostView.as_view(), name="delete_post"),
        
    path(r'post/<int:pk>/update', UpdatePostView.as_view(), name="update_post"),

    path(r'profile/<int:pk>/followers', ShowFollowersDetailView.as_view(), name="show_followers"),

    path(r'profile/<int:pk>/following', ShowFollowingDetailView.as_view(), name="show_following"),

    # Feed path for the logged-in user's profile
    path(r'profile/feed', PostFeedListView.as_view(), name="show_feed"),

    # Search path for the logged-in user
    path(r'profile/search', SearchView.as_view(), name="search"),

    #Auth
    path(r'login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html'), name="login"),
    path(r'logout/', auth_views.LogoutView.as_view(next_page='logout_confirmation'), name="logout"),
    path(r'logout_confirmation/', LogoutConfirmationView.as_view(), name="logout_confirmation"),

    # Create user and profile
    path(r'create_profile', CreateProfileView.as_view(), name="create_profile"),

    # Urls for "actions" between profiles
    path(r'profile/<int:pk>/follow', FollowProfile.as_view(), name="follow_profile"),
    path(r'profile/<int:pk>/delete_follow',DeleteFollowProfile.as_view(), name="delete_follow_profile"),
    path(r'profile/<int:pk>/like', LikePost.as_view(), name="like_post"),
    path(r'profile/<int:pk>/delete_like', DeleteLikePost.as_view(), name="delete_like_post"),
]