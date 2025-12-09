from rest_framework.generics import *
from rest_framework.generics import *
from django.db.models import Sum, Max, Count
from .models import Exercise
from .serializers import ExerciseSerializer,ScheduleSerializer, RoutineSerializer, RoutineItemSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.utils import timezone
from datetime import timedelta
from .models import TrainingSchedule, Routine, WorkoutSession, RoutineItem, WorkoutLog
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

# LIST VIEW: Returns all exercises (JSON)
class ExerciseList(ListCreateAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

# DETAIL VIEW: Returns one specific exercise (JSON)
class ExerciseDetail(RetrieveUpdateDestroyAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

class DashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated] 

    def get(self, request):
        #Find the Active Schedule for the logged in user
        active_schedule = TrainingSchedule.objects.filter(user=request.user, is_active=True).first()

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
            # Check if this routine has already been completed today
            is_completed = WorkoutSession.objects.filter(
                routine=routine_today,
                date=timezone.now().date()
            ).exists()

            today_data = {
                "id": routine_today.id,
                "name": routine_today.name,
                "is_completed": is_completed
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
        ).values('routine').distinct().count()

        # Total routines planned per week (Assuming 1 per routine)
        total_routines = Routine.objects.filter(schedule=active_schedule).count()

        # Weekly Time Spent
        total_minutes = WorkoutSession.objects.filter(
            routine__schedule=active_schedule,
            date__range=[start_of_week, end_of_week]
        ).aggregate(Sum('duration_minutes'))['duration_minutes__sum'] or 0

        # PR Spotlight (All-time best lift)
        pr_log = WorkoutLog.objects.order_by('-weight_used').first()
        pr_data = None
        if pr_log:
            pr_data = {
                "exercise": pr_log.exercise.name,
                "weight": pr_log.weight_used
            }

        server_time = timezone.now().isoformat()

        return Response({
            "schedule_name": active_schedule.name,
            "today_routine": today_data,
            "stats": {
                "completed": sessions_this_week,
                "total": total_routines,
                "weekly_minutes": total_minutes
            },
            "pr_spotlight": pr_data,
            "current_django_time": server_time
        })
    

# List all Schedules or Create a new one
class ScheduleList(ListCreateAPIView):
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        return TrainingSchedule.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Get details of ONE Schedule (with calendar data)
class ScheduleDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = ScheduleSerializer
    
    def get_queryset(self):
        return TrainingSchedule.objects.filter(user=self.request.user)

# Create a Routine inside a Schedule
class RoutineCreate(CreateAPIView):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer

# Retrieve, Update, or Delete a Routine
class RoutineDetail(RetrieveUpdateDestroyAPIView):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer
    permission_classes = [permissions.IsAuthenticated]

# Add an Exercise to a Routine
class RoutineItemCreate(CreateAPIView):
    queryset = RoutineItem.objects.all()
    serializer_class = RoutineItemSerializer

class ActiveSessionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        active_schedule = TrainingSchedule.objects.filter(user=request.user, is_active=True).first()
        if not active_schedule:
            return Response({"message": "No active schedule found"}, status=status.HTTP_404_NOT_FOUND)

        today_name = timezone.now().strftime('%A')
        routine = Routine.objects.filter(schedule=active_schedule, day_of_week=today_name).first()

        if not routine:
            return Response({"message": "No routine for today"}, status=status.HTTP_404_NOT_FOUND)

        # Check if already completed
        if WorkoutSession.objects.filter(routine=routine, date=timezone.now().date()).exists():
             return Response({"message": "Workout already completed today"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = RoutineSerializer(routine)
        return Response(serializer.data)

class SubmitWorkoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

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

class ConsistencyStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        active_schedule = TrainingSchedule.objects.filter(user=request.user, is_active=True).first()
        if not active_schedule:
            return Response({"completed": 0, "remaining": 0})

        # Calculate total weeks in schedule
        # Assuming schedule has start_date. If end_date is null, assume 12 weeks for calculation or just use current duration
        start_date = active_schedule.start_date
        end_date = active_schedule.end_date if active_schedule.end_date else timezone.now().date()
        
        # Total days active
        total_days = (end_date - start_date).days
        weeks = max(1, total_days // 7)
        
        # Routines per week
        routines_per_week = Routine.objects.filter(schedule=active_schedule).count()
        total_expected_workouts = weeks * routines_per_week

        # Completed workouts
        completed_workouts = WorkoutSession.objects.filter(routine__schedule=active_schedule).count()
        
        # Remaining (can be negative if they did extra, but let's clamp to 0)
        remaining = max(0, total_expected_workouts - completed_workouts)

        return Response({
            "completed": completed_workouts,
            "remaining": remaining,
            "schedule_name": active_schedule.name
        })

class ProgressionStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        exercise_id = request.query_params.get('exercise_id')
        if not exercise_id:
            return Response({"error": "Exercise ID required"}, status=status.HTTP_400_BAD_REQUEST)

        logs = WorkoutLog.objects.filter(exercise_id=exercise_id).order_by('session__date')
        
        data = []
        for log in logs:
            data.append({
                "date": log.session.date.strftime('%Y-%m-%d'),
                "weight": log.weight_used
            })
        
        return Response(data)

class MuscleGroupStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Count logs per muscle group
        # We want all muscle groups, even if 0, but for simplicity let's just count what's logged
        stats = WorkoutLog.objects.values('exercise__muscle_group').annotate(count=Count('id'))
        
        # Format for Recharts Radar: { subject: 'Chest', A: 10, fullMark: 150 }
        data = []
        max_val = 0
        for entry in stats:
            count = entry['count']
            if count > max_val: max_val = count
            data.append({
                "subject": entry['exercise__muscle_group'],
                "A": count,
                "fullMark": 0 # Will update
            })
        
        # Set fullMark slightly higher than max for better visual
        full_mark = max_val * 1.2 if max_val > 0 else 10
        for d in data:
            d['fullMark'] = full_mark
            
        return Response(data)

class ExerciseScatterView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        exercise_id = request.query_params.get('exercise_id')
        if not exercise_id:
            return Response([], status=400)
            
        logs = WorkoutLog.objects.filter(exercise_id=exercise_id)
        data = []
        for log in logs:
            data.append({
                "x": log.reps_achieved,
                "y": float(log.weight_used),
                "z": 1 # Size of bubble, could be set count or RPE
            })
            
            
        return Response(data)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email
        })

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        }, status=status.HTTP_201_CREATED)