from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from apps.carolerApi.caroler import new_music_caroler


# Create your views here.
def index(request):
    new_music_caroler()
    return render(request,'tzt.html')