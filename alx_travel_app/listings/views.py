from django.shortcuts import render

# Create your views here.
# listings/views.py
from django.http import JsonResponse

def home(request):
    return JsonResponse({"message": "ALX Travel API is running!"})
