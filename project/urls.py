# File: urls.py
# Author: Daniel Arteaga (d4nyart@bu.edu), 12/9/2025
# Description: URL configuration for the project app.
# Maps API endpoints to their respective views.

from django.urls import path, re_path
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    # Auth endpoints
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/api-token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),
    
    # Exercise endpoints
    path('api/exercises/', ExerciseList.as_view(), name='exercise_list'),
    path('api/exercises/<int:pk>/', ExerciseDetail.as_view(), name='exercise_detail'),
    
    # Dashboard endpoint
    path('api/dashboard/', DashboardView.as_view(), name='dashboard'),
    
    # Schedule and Routine endpoints
    path('api/schedules/', ScheduleList.as_view()),
    path('api/schedules/<int:pk>/', ScheduleDetail.as_view()),
    path('api/routines/create/', RoutineCreate.as_view()),
    path('api/routines/<int:pk>/', RoutineDetail.as_view()),
    path('api/items/create/', RoutineItemCreate.as_view()),
    
    # Workout Session endpoints
    path('api/active-session/', ActiveSessionView.as_view(), name='active_session'),
    path('api/submit-workout/', SubmitWorkoutView.as_view(), name='submit_workout'),
    
    # Stats endpoints
    path('api/stats/consistency/', ConsistencyStatsView.as_view(), name='stats_consistency'),
    path('api/stats/progression/', ProgressionStatsView.as_view(), name='stats_progression'),
    path('api/stats/muscle-groups/', MuscleGroupStatsView.as_view()),

    # Catch-all for React frontend
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]
