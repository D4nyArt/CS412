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
    
    def get_followers(self):
        """Return a list of Profile objects that follow this profile"""

        # Find all Follow objects where this profile is being followed
        follow_relationships = Follow.objects.filter(profile=self)
        
        follower_profiles = []

        # Extract the follower profiles from the Follow objects and convert to list
        for follow in follow_relationships:
            follower_profiles.append(follow.follower_profile)
        return follower_profiles
    
    def get_num_followers(self):
        """Return the number of followers for this profile"""
        return Follow.objects.filter(profile=self).count()
    
    def get_following(self):
        """Return a list of Profile objects that this profile follows"""

        # Find all Follow objects where this profile is the follower
        follow_relationships = Follow.objects.filter(follower_profile=self)
        
        following_profiles = []

        # Extract the profiles being followed from the Follow objects and convert to list
        for follow in follow_relationships:
            following_profiles.append(follow.profile)

        return following_profiles

    def get_num_following(self):
        return Follow.objects.filter(follower_profile=self).count()
    
    #Extra (not asked yet in assignements)
    def get_num_posts(self):
        print(Post.objects.filter(profile=self).count())
        return Post.objects.filter(profile=self).count()
    
    def get_post_feed(self):

        profiles_followed = self.get_following()

        post_of_followed = []

        for profile in profiles_followed:
            posts =  Post.objects.filter(profile=profile)
            post_of_followed.extend(posts)

        return post_of_followed 
    
    
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
    
    def get_all_comments(self):
        comments = Comment.objects.filter(post=self)
        return comments
    
    def get_likes(self):
        likes = Like.objects.filter(post=self)
        return likes


    #Extra
    def get_num_likes(self):
        return Like.objects.filter(post=self).count()

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
    

class Follow(models.Model):
    """Represent a follow relationship between two profiles"""
    
    # Foreign key to the profile being followed
    profile = models.ForeignKey(Profile, related_name="followed_by", on_delete=models.CASCADE)

    # Foreign key to the profile that is doing the following
    follower_profile = models.ForeignKey(Profile, related_name="following", on_delete=models.CASCADE)

    # Timestamp when the follow relationship was created
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return string representation of the follow relationship"""
        return f"{self.follower_profile} follows {self.profile}"
    
class Comment(models.Model):
    """Represent a comment on a post"""

    # Foreign key to the post this comment belongs to
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)

    # Foreign key to the profile that made this comment
    profile = models.ForeignKey(Profile, related_name="user_comments", on_delete=models.CASCADE)

    # Timestamp when the comment was created
    timestamp = models.DateTimeField(auto_now_add=True)

    # The actual comment text content
    text = models.TextField(blank=True)

    def __str__(self):
        """Return string representation of the comment"""
        return f"Comment {self.pk} by @{self.profile}"
    

class Like(models.Model):
    """Represent a like on a post"""

    # Foreign key to the post that was liked
    post = models.ForeignKey(Post, related_name="likes", on_delete=models.CASCADE)

    # Foreign key to the profile that liked the post
    profile = models.ForeignKey(Profile, related_name="user_likes", on_delete=models.CASCADE)

    # Timestamp when the like was created
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return string representation of the like"""
        return f"Like {self.pk} by @{self.profile} on {self.post}"