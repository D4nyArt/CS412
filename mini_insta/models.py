# File: models.py
# Author: Daniel Arteaga (d4nyart@bu.edu), 09/24/2025 
# Description: Django models for the Mini Instagram application.
# Contains the Profile model that represents user profiles with
# username, display name, profile image, bio, and join date.

from django.db import models

# Create your models here.


class Profile(models.Model): 
    """Encapsulate the data of a Profile of a person.
    
    This model represents a user profile in our Mini Instagram application,
    storing information about each user including their username,
    display name, profile image URL, biographical text, and join date.
    """
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    # URL pointing to the user's profile image
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)    
    # Automatically set to current date/time when profile is created
    join_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return string representation of the profile."""
        return f"{self.username}"
    
    def get_all_posts(self):
        posts = Post.objects.filter(profile=self)
        return posts
    

    
class Post(models.Model):
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    caption = models.TextField(blank=True)

    def __str__(self):
        return f"Post of profile: {self.profile}"
    
    def get_all_photos(self):
        photos = Photo.objects.filter(post=self)
        return photos
    
    def get_first_photo(self):
        """Return the first Photo object related to this post, or None if none exist."""
        photos = Photo.objects.filter(post=self)
        return photos.first()
    
class Photo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Photo of post: {self.post}"
    
