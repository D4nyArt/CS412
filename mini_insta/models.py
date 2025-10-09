# File: models.py
# Author: Daniel Arteaga (d4nyart@bu.edu), 09/24/2025
# Description: Django models for the Mini Instagram application.
# Contains the Profile, Post, and Photo models that represent user profiles,
# posts, and associated photos.

from django.db import models
from django.urls import reverse

# Create your models here.

class Profile(models.Model): 
    """Encapsulate the data of a Profile of a person"""

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
    
    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk':self.pk})
    
    def get_all_posts(self):
        """Return all posts associated with this profile."""
        posts = Post.objects.filter(profile=self)
        return posts

class Post(models.Model):
    """Model representing a post made by a user profile, encapsulating its data"""
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)  # The profile that created the post
    timestamp = models.DateTimeField(auto_now=True) 
    caption = models.TextField(blank=True) 

    def __str__(self):
        """Return string representation of the post"""
        return f"Post {self.pk}"
    
    def get_absolute_url(self):
        return reverse('show_post', kwargs={'pk':self.pk})
    
    def get_all_photos(self):
        """Return all photos objects associated with this post"""
        photos = Photo.objects.filter(post=self)
        return photos
    
    def get_first_photo(self):
        """Return the first Photo object related to this post, or None if it doesnt exist"""
        photos = Photo.objects.filter(post=self)
        return photos.first()
    
class Photo(models.Model):
    """Model representing a photo attached to a post encapsulating its data"""
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # The post this photo belongs to
    image_url = models.URLField(blank=True) 
    timestamp = models.DateTimeField(auto_now=True)

    image_file = models.ImageField(blank=True)

    def __str__(self):
        """Return string representation of the photo based on how the image is stored"""
        if self.image_url:
            return f"Photo {self.pk} (URL: {self.image_url})"
        elif self.image_file:
            return f"Photo {self.pk} (File: {self.image_file.name})"
        else:
            return f"Photo {self.pk} (No image)"
    
    def get_image_url(self):
        """Return the URL to the image, either from image_url or image_file"""
        if self.image_url:
            return self.image_url
        elif self.image_file:
            return self.image_file.url
        else:
            return None
    
