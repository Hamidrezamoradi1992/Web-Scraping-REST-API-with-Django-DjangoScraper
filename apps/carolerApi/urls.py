from django.urls import path

from apps.carolerApi import views

urlpatterns = [
    path('', views.index, name='caroler-api'),
]