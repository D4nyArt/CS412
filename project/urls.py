from django.urls import path
from .views import ExerciseList, ExerciseDetail

urlpatterns = [
    path('api/exercises/', ExerciseList.as_view(), name='exercise_list'),
    path('api/exercises/<int:pk>/', ExerciseDetail.as_view(), name='exercise_detail'),
]