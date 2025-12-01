from django.urls import path
from .views import *

urlpatterns = [
    path('api/exercises/', ExerciseList.as_view(), name='exercise_list'),
    path('api/exercises/<int:pk>/', ExerciseDetail.as_view(), name='exercise_detail'),
    path('api/dashboard/', DashboardView.as_view(), name='dashboard'),
    
    path('api/schedules/', ScheduleList.as_view()),
    path('api/schedules/<int:pk>/', ScheduleDetail.as_view()),
    path('api/routines/create/', RoutineCreate.as_view()),
    path('api/routines/<int:pk>/', RoutineDetail.as_view()),
    path('api/items/create/', RoutineItemCreate.as_view()),
    path('api/active-session/', ActiveSessionView.as_view(), name='active_session'),
    path('api/submit-workout/', SubmitWorkoutView.as_view(), name='submit_workout'),
    path('api/stats/consistency/', ConsistencyStatsView.as_view(), name='stats_consistency'),
    path('api/stats/progression/', ProgressionStatsView.as_view(), name='stats_progression'),
]