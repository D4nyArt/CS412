from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Exercise)
admin.site.register(TrainingSchedule)
admin.site.register(Routine)
admin.site.register(RoutineItem)
admin.site.register(WorkoutSession)
admin.site.register(WorkoutLog)
