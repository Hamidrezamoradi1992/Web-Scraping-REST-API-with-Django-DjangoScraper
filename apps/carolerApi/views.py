from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from apps.carolerApi.models import Category, Music
from rest_framework import status
from apps.carolerApi.serializers import MusicSerializers
from django.db.models import Q
from rest_framework.throttling import AnonRateThrottle
from .caroler import CarolerApi
from apps.account.throttling import VipThrottling, UsersThrottle
from rest_framework.permissions import IsAuthenticated
from apps.account.permissions import VipPermission
from rest_framework.authentication import BasicAuthentication, SessionAuthentication


# Create your views here.

# @method_decorator(cache_page(60 * 10), name='get')
class MusicCarolerApiListView(ListAPIView):
    queryset = Music.objects.all().order_by('music_category')
    serializer_class = MusicSerializers
    throttle_classes = [AnonRateThrottle, UsersThrottle, VipThrottling]
    permission_classes = [IsAuthenticated, VipPermission]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get(self, request: Request, **kwargs):
        CarolerApi.new_music()
        return Response(self.serializer_class(self.get_queryset(), many=True).data)


class SearchMusicView(APIView):
    throttle_classes = [UsersThrottle, VipThrottling]
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

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
        CarolerApi.search_music(context=search_title)
        music = Music.objects.filter(Q(title_music__icontains=title) |
                                     Q(actor_name__icontains=actor)) if title in ['البوم', 'آلبوم'] else (
            Music.objects.filter(actor_name=actor))
        print(title in ['البوم', 'آلبوم'])
        if music.exists():
            serializer = MusicSerializers(music, many=True)
            return Response(serializer.data)
        return Response({'message': 'nodata'}, status=status.HTTP_404_NOT_FOUND)


# @method_decorator(cache_page(10), name='dispatch')
class SearchMusicCategoryView(APIView):
    throttle_classes = [AnonRateThrottle, UsersThrottle, VipThrottling]
    authentication_classes = []
    permission_classes = []

    def get(self, request: Request, category):
        category = Category.objects.filter(title__icontains=category)
        if category.exists():
            music = Music.objects.filter(music_category__in=category)
            serializer = MusicSerializers(music, many=True)
            return Response(serializer.data)
        return Response({'message': 'nodata'}, status=status.HTTP_404_NOT_FOUND)
