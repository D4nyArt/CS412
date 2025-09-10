# File: views.py
# Author: Dany Art (d4nyart@bu.edu), 9/10/2025
# Description: Django view functions for the quotes app. Selects a random
# quote and image and renders templates for single-quote, all-quotes, and about.

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random 

# Constants: lists of quotes and image URLs used by the views.
ALAN_TURING_QUOTES = [
    "Sometimes it is the people no one can imagine anything of who do the things no one can imagine.",
    "We can only see a short distance ahead, but we can see plenty there that needs to be done.",
    "Those who can imagine anything, can create the impossible.",
    "A computer would deserve to be called intelligent if it could deceive a human into believing that it was human.",
    "If a machine is expected to be infallible, it cannot also be intelligent.",
    "The original question, 'Can machines think?' I believe to be too meaningless to deserve discussion.",
    "One day ladies will take their computers for walks in the park and tell each other, 'My little computer said such a funny thing this morning'.",
    "It is not possible to produce a set of rules purporting to describe what a man should do in every conceivable set of circumstances."
]

ALAN_TURING_IMAGES = [
    "https://cdn.britannica.com/81/191581-050-8C0A8CD3/Alan-Turing.jpg",
    "https://scx1.b-cdn.net/csz/news/800a/2012/alanturingat.jpg",
    "https://preview.redd.it/51dcpxhdwcox.jpg?width=640&crop=smart&auto=webp&s=c9cd2a728bad539bce6fa2c17f4589ac763b4216",
    "https://spectrum.ieee.org/media-library/f1.jpg?id=25583742&width=1240&quality=85",
    "https://oldshirburnian.org.uk/wp-content/uploads/2023/02/Alan-Turing-Sherborne-School-Summer-term-1927-768x989.jpg"
]

# Create your views here.
def quote(request):
    """Render a page with one randomly selected quote and image."""
    # Choose one quote and one image at random for the view.
    selected_quote = random.choice(ALAN_TURING_QUOTES)
    selected_image = random.choice(ALAN_TURING_IMAGES)
    template_name = "quotes/quote.html"
    
    # Context passed to the template.
    context = {
        "quote": selected_quote,
        "image": selected_image
    }
    return render(request, template_name, context)

def show_all(request):
    """Render a page showing all quotes and all images."""
    # Provide the full lists so the template can iterate over them.
    
    template_name = "quotes/show_all.html"
    context = {
        "quotes": ALAN_TURING_QUOTES,
        "images": ALAN_TURING_IMAGES
    }
    return render(request, template_name, context)

def about(request):
    """Render the about page for the quotes app."""
    # No additional context required.
    template_name = "quotes/about.html"
    return render(request, template_name)  
