from django.urls import path

from apps.carolerApi import views

urlpatterns = [
    path('api/', views.MusicCarolerApiListView.as_view(), name='caroler-api'),
    path('api/search/<str:actors>', views.SearchMusicView.as_view(), name='caroler-api'),

]