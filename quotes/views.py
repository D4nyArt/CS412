from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time

# Create your views here.

def home(request):
    template_name = "quotes/home.html"

    return render(request, template_name)

