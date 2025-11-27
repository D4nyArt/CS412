from django.db import models
from django.contrib.auth.models import User

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    muscle_group = models.CharField(max_length=50) # e.g. Chest, Legs

    def __str__(self):
        return f"{self.name} ({self.muscle_group})"

class TrainingSchedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100) # e.g. Winter Bulk
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Routine(models.Model):
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
        return f"{self.name} ({self.day_of_week})"

class RoutineItem(models.Model):
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE, related_name='items')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    target_sets = models.IntegerField()
    target_reps = models.IntegerField()
    target_weight = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    order = models.IntegerField(default=0) # For sorting

    def __str__(self):
        return f"{self.exercise.name} in {self.routine.name}"

class WorkoutSession(models.Model):
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    duration_minutes = models.IntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Session: {self.routine.name} on {self.date}"

class WorkoutLog(models.Model):
    session = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE, related_name='logs')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    weight_used = models.DecimalField(max_digits=6, decimal_places=2) # Supports 135.5 for instance
    reps_achieved = models.IntegerField()

    def __str__(self):
        return f"{self.exercise.name} - {self.weight_used}lbs"