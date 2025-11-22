from rest_framework.generics import *
from .models import Exercise
from .serializers import ExerciseSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.utils import timezone
from datetime import timedelta
from .models import TrainingSchedule, Routine, WorkoutSession

# LIST VIEW: Returns all exercises (JSON)
class ExerciseList(ListAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

# DETAIL VIEW: Returns one specific exercise (JSON)
class ExerciseDetail(RetrieveAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

class DashboardView(APIView):
    # For now, allowing any access so  test easily without login setup
    permission_classes = [permissions.AllowAny] 

    def get(self, request):
        #Find the Active Schedule (just getting the first active one found)
        active_schedule = TrainingSchedule.objects.filter(is_active=True).first()

        if not active_schedule:
            return Response({
                "schedule_name": "No Active Schedule",
                "today_routine": None,
                "stats": {"completed": 0, "total": 0}
            })

        # Determine Today's Routine
        # strftime('%A') returns 'Monday', 'Tuesday', etc.
        today_name = timezone.now().strftime('%A') 
        
        routine_today = Routine.objects.filter(
            schedule=active_schedule, 
            day_of_week=today_name
        ).first()

        today_data = None
        if routine_today:
            today_data = {
                "id": routine_today.id,
                "name": routine_today.name
            }

        # Calculate Quick Stats (Workouts this week)
        today_date = timezone.now().date()
        # Find Monday of current week
        start_of_week = today_date - timedelta(days=today_date.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        # Count how many sessions happened this week for this schedule
        sessions_this_week = WorkoutSession.objects.filter(
            routine__schedule=active_schedule,
            date__range=[start_of_week, end_of_week]
        ).count()

        # Total routines planned per week (Assuming 1 per routine)
        total_routines = Routine.objects.filter(schedule=active_schedule).count()

        server_time = timezone.now().isoformat()

        return Response({
            "schedule_name": active_schedule.name,
            "today_routine": today_data,
            "stats": {
                "completed": sessions_this_week,
                "total": total_routines
            },
            "current_django_time": server_time
        })