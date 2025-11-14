from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    # Regular views
    path('', views.random_joke_picture, name='random_joke_picture'),
    path('random', views.random_joke_picture, name='random'),
    path('jokes', views.JokeListView.as_view(), name='all_jokes'),
    path('joke/<int:pk>', views.JokeDetailView.as_view(), name='joke_detail'),
    path('pictures', views.PictureListView.as_view(), name='all_pictures'),
    path('picture/<int:pk>', views.PictureDetailView.as_view(), name='picture_detail'),
    
    # API endpoints
    path('api/', api_views.RandomJokeAPIView.as_view(), name='api_random_joke'),
    path('api/random', api_views.RandomJokeAPIView.as_view(), name='api_random'),
    path('api/jokes', api_views.JokeListCreateAPIView.as_view(), name='api_jokes'),
    path('api/joke/<int:pk>', api_views.JokeDetailAPIView.as_view(), name='api_joke_detail'),
    path('api/pictures', api_views.PictureListAPIView.as_view(), name='api_pictures'),
    path('api/picture/<int:pk>', api_views.PictureDetailAPIView.as_view(), name='api_picture_detail'),
    path('api/random_picture', api_views.RandomPictureAPIView.as_view(), name='api_random_picture'),
]
