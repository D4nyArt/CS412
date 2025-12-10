# File: admin.py
# Author: Daniel Arteaga (d4nyart@bu.edu), 12/9/2025
# Description: Admin configuration for the project application.

from django.contrib import admin
from .models import *

# Register your models here.

# Register the Exercise model
admin.site.register(Exercise)

# Register the TrainingSchedule model
admin.site.register(TrainingSchedule)

# Register the Routine model
admin.site.register(Routine)

# Register the RoutineItem model
admin.site.register(RoutineItem)

# Register the WorkoutSession model
admin.site.register(WorkoutSession)

# Register the WorkoutLog model
admin.site.register(WorkoutLog)
