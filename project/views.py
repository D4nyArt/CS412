from rest_framework.generics import *
from .models import Exercise
from .serializers import ExerciseSerializer,ScheduleSerializer, RoutineSerializer, RoutineItemSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.utils import timezone
from datetime import timedelta
from .models import TrainingSchedule, Routine, WorkoutSession, RoutineItem, WorkoutLog

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
    

# List all Schedules or Create a new one
class ScheduleList(ListCreateAPIView):
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        # FIX: Check if user is logged in. 
        # If yes, filter by their ID. 
        # If no (React dev mode), return ALL schedules so the UI shows something.
        if self.request.user.is_authenticated:
            return TrainingSchedule.objects.filter(user=self.request.user)
        else:
            return TrainingSchedule.objects.all() # Return everything for testing

    def perform_create(self, serializer):
        # FIX: Handle creation for anonymous users (assign to the first admin user found)
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            # Just for testing: assign to the first user in the DB (your admin)
            from django.contrib.auth.models import User
            first_user = User.objects.first()
            serializer.save(user=first_user)

# Get details of ONE Schedule (with calendar data)
class ScheduleDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = ScheduleSerializer
    
    def get_queryset(self):
        # Same fix here
        if self.request.user.is_authenticated:
            return TrainingSchedule.objects.filter(user=self.request.user)
        else:
            return TrainingSchedule.objects.all()

# Create a Routine inside a Schedule
class RoutineCreate(CreateAPIView):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer

# Add an Exercise to a Routine
class RoutineItemCreate(CreateAPIView):
    queryset = RoutineItem.objects.all()
    serializer_class = RoutineItemSerializer

class ActiveSessionView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        active_schedule = TrainingSchedule.objects.filter(is_active=True).first()
        if not active_schedule:
            return Response({"message": "No active schedule found"}, status=status.HTTP_404_NOT_FOUND)

        today_name = timezone.now().strftime('%A')
        routine = Routine.objects.filter(schedule=active_schedule, day_of_week=today_name).first()

        if not routine:
            return Response({"message": "No routine for today"}, status=status.HTTP_404_NOT_FOUND)

        serializer = RoutineSerializer(routine)
        return Response(serializer.data)

class SubmitWorkoutView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        routine_id = data.get('routine_id')
        duration = data.get('duration')
        notes = data.get('notes')
        logs = data.get('logs', [])

        try:
            routine = Routine.objects.get(id=routine_id)
        except Routine.DoesNotExist:
            return Response({"error": "Routine not found"}, status=status.HTTP_404_NOT_FOUND)

        # Create Session
        session = WorkoutSession.objects.create(
            routine=routine,
            duration_minutes=duration,
            notes=notes
        )

        # Create Logs and Update Targets
        for log_data in logs:
            exercise_id = log_data.get('exercise_id')
            weight = log_data.get('weight')
            reps = log_data.get('reps')

            try:
                exercise = Exercise.objects.get(id=exercise_id)
            except Exercise.DoesNotExist:
                continue
            
            WorkoutLog.objects.create(
                session=session,
                exercise=exercise,
                weight_used=weight,
                reps_achieved=reps
            )

            # Auto-increment logic
            routine_item = RoutineItem.objects.filter(routine=routine, exercise=exercise).first()
            if routine_item:
                # Check if they met the target
                # Note: target_weight defaults to 0.0 if not set, so we should check > 0 or just assume valid
                if float(weight) >= routine_item.target_weight and int(reps) >= routine_item.target_reps:
                    # Simple progression: Add 5lbs
                    routine_item.target_weight = float(routine_item.target_weight) + 5.0
                    routine_item.save()

        return Response({"message": "Workout saved successfully"}, status=status.HTTP_201_CREATED)