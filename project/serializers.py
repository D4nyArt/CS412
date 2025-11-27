from rest_framework import serializers
from .models import Exercise
from .models import TrainingSchedule, Routine, RoutineItem, Exercise
class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'name', 'muscle_group']

class RoutineItemSerializer(serializers.ModelSerializer):
    exercise_name = serializers.CharField(source='exercise.name', read_only=True)
    
    class Meta:
        model = RoutineItem
        # Add 'routine' to the list for creating at the same time routine and routine items
        fields = ['id', 'routine', 'exercise', 'exercise_name', 'target_sets', 'target_reps', 'order']

class RoutineSerializer(serializers.ModelSerializer):
    items = RoutineItemSerializer(many=True, read_only=True)

    class Meta:
        model = Routine
        # Add 'schedule' here so we can send it from React
        fields = ['id', 'schedule', 'name', 'day_of_week', 'items']

class ScheduleSerializer(serializers.ModelSerializer):
    # This fetches the routines linked to this schedule automatically
    routines = RoutineSerializer(many=True, read_only=True)
    class Meta:
        model = TrainingSchedule
        fields = ['id', 'name', 'start_date', 'end_date', 'is_active', 'routines']

        