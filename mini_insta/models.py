# File: models.py
# Author: Daniel Arteaga (d4nyart@bu.edu), 09/24/2025
# Description: Django models for the Mini Instagram application.
# Contains the Profile, Post, and Photo models that represent user profiles,
# posts, and associated photos.

from django.db import models
from django.urls import reverse

# Create your models here.

class Profile(models.Model): 
    """Represent a user profile in the Mini Instagram application.
    
    Encapsulates all user profile data including username, display name,
    profile image, bio text, and join date information.
    """
    username = models.TextField(blank=True) 
    
    display_name = models.TextField(blank=True)

    profile_image_url = models.URLField(blank=True)

    bio_text = models.TextField(blank=True) 

    join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return string representation of the profile"""
        return f"{self.username}"
    
    def get_absolute_url(self):
        """Return the URL for this profile's detail page"""
        return reverse('show_profile', kwargs={'pk':self.pk})
    
    def get_all_posts(self):
        """Return all posts associated with this profile"""
        posts = Post.objects.filter(profile=self)
        return posts

class Post(models.Model):
    """Represent a post created by a user profile

    Contains the post's content, timestamp, and association with the
    profile that created it. Can have multiple photos attached.
    """
    
    # Foreign key linking this post to the profile that created it
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)  
    
    timestamp = models.DateTimeField(auto_now_add=True) 
    
    caption = models.TextField(blank=True) 

    def __str__(self):
        """Return string representation of the post"""
        return f"Post {self.pk}"
    
    def get_absolute_url(self):
        """Return the URL for this post's detail page"""
        return reverse('show_post', kwargs={'pk':self.pk})
    
    def get_all_photos(self):
        """Return all Photo objects related to this post"""
        photos = Photo.objects.filter(post=self)
        return photos
    
    def get_first_photo(self):
        """Return the first Photo object related to this post, or None if it does not exist."""
        photos = Photo.objects.filter(post=self)
        return photos.first()
    
class Photo(models.Model):
    """Represent a Photo attached to a post
    
    Handles both URL-based images and uploaded image files, allowing posts
    to display photos from external URLs or user-uploaded files.
    """
    
    # Foreign key linking this photo to the post it belongs to
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  
    
    image_url = models.URLField(blank=True) 
    
    timestamp = models.DateTimeField(auto_now=True)

    # Uploaded image file 
    image_file = models.ImageField(blank=True)

    def __str__(self):
        """Return string representation showing how the image is stored"""
        # Check which type of image storage is being used
        if self.image_url:
            return f"Photo {self.pk} (URL: {self.image_url})"
        elif self.image_file:
            return f"Photo {self.pk} (File: {self.image_file.name})"
        else:
            return f"Photo {self.pk} (No image)"
    
    def get_image_url(self):
        """Return the appropriate URL to display the image
        
        Checks both image_url and image_file fields and returns the
        appropriate URL for template rendering
        """
        if self.image_url:
            return self.image_url
        elif self.image_file:
            return self.image_file.url
        else:
            return None
    
