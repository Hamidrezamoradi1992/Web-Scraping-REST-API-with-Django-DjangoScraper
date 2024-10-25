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
from django.db.models import Q
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


# Create your views here.

@method_decorator(cache_page(10), name='dispatch')
class MusicCarolerApiListView(ListAPIView):
    queryset = Music.objects.all().order_by('music_category')
    serializer_class = MusicSerializers
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self, request: Request):
        new_music_caroler()
        return Response(self.serializer_class(self.get_queryset(), many=True).data)


class SearchMusicView(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self, request: Request, actors=None):
        title = actors.strip().split('،')[1]
        actor = actors.strip().split('،')[0]
        print('a', actor, "\n", len(title))
        music = Music.objects.filter(actor_name__icontains=actor)
        if music.exists():
            if len(title) == 0:
                serializer = MusicSerializers(music, many=True)
                return Response(serializer.data)
            m = music.filter(title_music__icontains=title)
            if m.exists():
                serializer = MusicSerializers(m, many=True)
                return Response(serializer.data)

        search_title = f'{title} {actor}'
        flag = searchmusic(title=search_title)
        if flag:
            music = Music.objects.filter(title_music__icontains=title, actor_name__icontains=actor)
            serializer = MusicSerializers(music, many=True)
            return Response(serializer.data)

        return Response({'message': 'nodata'}, status=status.HTTP_404_NOT_FOUND)


class SearchMusicCategoryView(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self, request: Request, category):
        category = Category.objects.filter(title__icontains=category)
        if category.exists():
            music = Music.objects.filter(music_category__in=category)
            serializer = MusicSerializers(music, many=True)
            return Response(serializer.data)
        return Response({'message': 'nodata'}, status=status.HTTP_404_NOT_FOUND)
