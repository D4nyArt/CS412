# File: serializers.py
# Author: Daniel Arteaga (d4nyart@bu.edu), 12/9/2025
# Description: DRF Serializers for converting model instances to JSON and vice-versa.

from rest_framework import serializers
from .models import TrainingSchedule, Routine, RoutineItem, Exercise

class ExerciseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Exercise model.
    """
    class Meta:
        model = Exercise
        fields = ['id', 'name', 'muscle_group']

class RoutineItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the RoutineItem model.
    Includes the exercise name as a read-only field for convenience.
    """
    exercise_name = serializers.CharField(source='exercise.name', read_only=True)
    
    class Meta:
        model = RoutineItem
        # Add 'routine' to the list for creating at the same time routine and routine items
        fields = ['id', 'routine', 'exercise', 'exercise_name', 'target_sets', 'target_reps', 'target_weight', 'order']

class RoutineSerializer(serializers.ModelSerializer):
    """
    Serializer for the Routine model.
    Nested includes related RoutineItems (read-only).
    """
    items = RoutineItemSerializer(many=True, read_only=True)

    class Meta:
        model = Routine
        # Add 'schedule' here so we can send it from React
        fields = ['id', 'schedule', 'name', 'day_of_week', 'items']

class ScheduleSerializer(serializers.ModelSerializer):
    """
    Serializer for the TrainingSchedule model.
    Nested includes related Routines (read-only).
    """
    # This fetches the routines linked to this schedule automatically
    routines = RoutineSerializer(many=True, read_only=True)
    class Meta:
        model = TrainingSchedule
        fields = ['id', 'name', 'start_date', 'end_date', 'is_active', 'routines']