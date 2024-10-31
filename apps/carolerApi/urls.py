from django.urls import path

from apps.carolerApi import views

urlpatterns = [
    path('api/music/new/tracks', views.MusicNewTracksApiListView.as_view()),
    path('api/music/all/tracks', views.MusicAllTracksApiListView.as_view()),
    path('api/music/search/<str:actors>', views.SearchMusicView.as_view()),
    path('api/music/search/category/<str:category>', views.SearchMusicCategoryView.as_view()),
]