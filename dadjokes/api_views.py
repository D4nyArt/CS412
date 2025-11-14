from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Joke, Picture
from .serializers import JokeSerializer, PictureSerializer
import random


class RandomJokeAPIView(APIView):
    """API endpoint that returns a random Joke"""
    
    def get(self, request):
        jokes = Joke.objects.all()
        joke = random.choice(jokes)
        serializer = JokeSerializer(joke)
        return Response(serializer.data)
    

class JokeListCreateAPIView(generics.ListCreateAPIView):
    """API endpoint that allows listing all Jokes and creating new Jokes"""
    
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer


class JokeDetailAPIView(generics.RetrieveAPIView):
    """API endpoint that returns a single Joke by primary key"""
    
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer


class PictureListAPIView(generics.ListAPIView):
    """API endpoint that returns all Pictures"""
    
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class PictureDetailAPIView(generics.RetrieveAPIView):
    """API endpoint that returns a single Picture by primary key"""
    
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class RandomPictureAPIView(APIView):
    """API endpoint that returns a random Picture"""
    def get(self, request):
        pictures = Picture.objects.all()
        picture = random.choice(pictures)
        serializer = PictureSerializer(picture)
        return Response(serializer.data)
