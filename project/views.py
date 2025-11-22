from rest_framework.generics import *
from .models import Exercise
from .serializers import ExerciseSerializer

# LIST VIEW: Returns all exercises (JSON)
class ExerciseList(ListCreateAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

# DETAIL VIEW: Returns one specific exercise (JSON)
class ExerciseDetail(RetrieveUpdateDestroyAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer