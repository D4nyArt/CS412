from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Joke, Picture
import random

# Create your views here.

def random_joke_picture(request):
    """Show one random Joke and one random Picture"""
    jokes = Joke.objects.all()
    pictures = Picture.objects.all()
    
    joke = random.choice(jokes) if jokes else None
    picture = random.choice(pictures) if pictures else None
    
    context = {
        'joke': joke,
        'picture': picture,
    }
    return render(request, 'dadjokes/random.html', context)


class JokeListView(ListView):
    """Show all Jokes"""
    model = Joke
    template_name = 'dadjokes/all_jokes.html'
    context_object_name = 'jokes'


class JokeDetailView(DetailView):
    """Show one Joke by primary key"""
    model = Joke
    template_name = 'dadjokes/joke_detail.html'
    context_object_name = 'joke'


class PictureListView(ListView):
    """Show all Pictures"""
    model = Picture
    template_name = 'dadjokes/all_pictures.html'
    context_object_name = 'pictures'


class PictureDetailView(DetailView):
    """Show one Picture by primary key"""
    model = Picture
    template_name = 'dadjokes/picture_detail.html'
    context_object_name = 'picture'
