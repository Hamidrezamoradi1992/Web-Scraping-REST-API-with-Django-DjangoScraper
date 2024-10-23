from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from apps.carolerApi.caroler import new_music_caroler, searchmusic
from apps.carolerApi.models import Category, Music
from rest_framework import status
from apps.carolerApi.serializers import MusicSerializers


# Create your views here.

@method_decorator(cache_page(10), name='dispatch')
class MusicCarolerApiListView(ListAPIView):
    queryset = Music.objects.all().order_by('music_category')
    serializer_class = MusicSerializers

    def get(self, request:Request):
        new_music_caroler()
        return Response(self.serializer_class(self.get_queryset(), many=True).data)


