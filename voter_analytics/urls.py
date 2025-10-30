# File: urls.py
# Author: Daniel Arteaga Mercado (d4nyart@bu.edu), 10/30/2025
# Description: URL configuration for voter analytics application.
#  Maps URL patterns to views for voter list, voter detail, and data visualization pages.

from django.urls import path
from .views import *

urlpatterns = [
    # Main voter list page with filtering options
    path(r'', VoterListView.as_view(), name='voters'),
    
    # Individual voter detail page
    path(r'voter/<int:pk>', VoterDetailView.as_view(), name='show_voter'),
    
    # Data visualization graphs page
    path(r'graphs', VoterListGraphsView.as_view(), name='graphs'),
]