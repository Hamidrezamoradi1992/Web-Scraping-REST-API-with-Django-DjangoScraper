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


class SearchMusicView(APIView):
    def get(self, request:Request, actor=None, title=None):
        music = Music.objects.filter(actor_name__icontains=actor)
        if music.exists():
            music_title = music.filter(title_music__icontains=title)
            if music_title.exists():
                serializer = MusicSerializers(music_title, many=True)
                return Response(serializer.data)
        flag = searchmusic(title=title, actor=actor)
        if flag:
            music = Music.objects.filter(title_music=title, actor_name=actor)
            serializer = MusicSerializers(music, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)