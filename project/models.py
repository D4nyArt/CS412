# File: models.py
# Author: Daniel Arteaga (d4nyart@bu.edu), 12/9/2025
# Description: Database models for the workout planner application.
# This file defines the data structure for Users, Exercises, Schedules, and Workouts.
# It includes more than 4 models with foreign-key relationships.

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Exercise(models.Model):
    """
    Represents a specific physical exercise.
    This model can exist independently (no foreign keys required),
    but is referred to by RoutineItem and WorkoutLog.
    """
    name = models.CharField(max_length=100)
    muscle_group = models.CharField(max_length=50) # e.g. Chest, Legs

    def __str__(self):
        """Return a string representation of the exercise."""
        return f"{self.name} ({self.muscle_group})"

class TrainingSchedule(models.Model):
    """
    Represents a user's training plan for a period of time.
    Has a foreign key to User.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100) # e.g. Winter Bulk
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        """Return the name of the schedule as its string representation."""
        return self.name

class Routine(models.Model):
    """
    Represents a single workout routine (e.g., 'Leg Day') assigned to a specific day of the week.
    Linked to a TrainingSchedule.
    """
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    schedule = models.ForeignKey(TrainingSchedule, on_delete=models.CASCADE, related_name='routines')
    name = models.CharField(max_length=100) # e.g. Leg Day
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)

    def __str__(self):
        """Return the routine name and day as string."""
        return f"{self.name} ({self.day_of_week})"

class RoutineItem(models.Model):
    """
    Represents an exercise within a routine, including target sets, reps, and weight.
    Links a Routine to an Exercise.
    """
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE, related_name='items')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    target_sets = models.IntegerField()
    target_reps = models.IntegerField()
    target_weight = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    order = models.IntegerField(default=0) # For sorting exercises within a routine

    def __str__(self):
        """Return a description of the exercise in the routine."""
        return f"{self.exercise.name} in {self.routine.name}"

class WorkoutSession(models.Model):
    """
    Represents an actual performed workout session based on a routine.
    Tracks when the workout happened and any optional notes.
    """
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    duration_minutes = models.IntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        """Return a summary of the session."""
        return f"Session: {self.routine.name} on {self.date}"

class WorkoutLog(models.Model):
    """
    Represents the actual performance of a specific exercise during a session.
    Tracks weight used and reps achieved.
    """
    session = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE, related_name='logs')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    weight_used = models.DecimalField(max_digits=6, decimal_places=2) # Supports fractions like 135.5
    reps_achieved = models.IntegerField()

    def __str__(self):
        """Return a summary of the performance."""
        return f"{self.exercise.name} - {self.weight_used}lbs"