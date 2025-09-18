# File: urls.py
# Author: Daniel Arteaga (dany@bu.edu), 9/12/2025
# Description: URL patterns for the restaurant Django app, 
# mapping URLs to view functions.

from django.urls import path
from . import views

urlpatterns = [
    # Main page
    path('', views.main, name="main"),
    path('main/', views.main, name="main"),
    # Order form page
    path('order/', views.order, name="order"),
    # Order confirmation page
    path('confirmation/', views.confirmation, name="confirmation"),
]
