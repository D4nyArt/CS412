# File: urls.py
# Author: Daniel Arteaga (d4nyart@bu.edu), 9/10/2025
# Description: URL patterns for the quotes app (random quote, all quotes, about).

"""Define URL routes for the quotes application."""

from django.urls import path
from . import views

# URL patterns for the quotes app.
# Each path maps a short URL to a view function in views.py.
urlpatterns = [
    # Root of the app, random quote view.
    path('', views.quote, name='quote'),

    # Explicit 'quote/' route, same random quote view.
    path('quote/', views.quote, name='quote'),

    # Page showing all quotes and images.
    path('show_all/', views.show_all, name='show_all'),

    # Static about page for the app.
    path('about/', views.about, name='about'),
]
