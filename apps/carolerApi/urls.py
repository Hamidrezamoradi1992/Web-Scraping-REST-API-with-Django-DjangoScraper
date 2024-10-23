from django.urls import path

from apps.carolerApi import views

urlpatterns = [
    path('api/', views.MusicCarolerApiListView.as_view(), name='caroler-api'),
    path('api/serch/<str:actor>/<str:title>', views.SearchMusicView.as_view(), name='caroler-api'),

]