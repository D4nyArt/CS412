from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.

def home(request):
    response_text = """
    <html><h1>Welcome to the Quotes Home Page!</h1></html>
    """

    return HttpResponse(response_text)

