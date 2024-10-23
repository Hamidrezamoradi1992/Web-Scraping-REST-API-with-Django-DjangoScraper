from django.urls import path

from apps.carolerApi import views

urlpatterns = [
    path('api/', views.MusicCarolerApiListView.as_view(), name='caroler-api'),
]