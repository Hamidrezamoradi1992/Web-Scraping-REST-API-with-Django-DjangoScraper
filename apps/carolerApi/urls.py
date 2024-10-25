from django.urls import path

from apps.carolerApi import views

urlpatterns = [
    path('api/', views.MusicCarolerApiListView.as_view()),
    path('api/search/<str:actors>', views.SearchMusicView.as_view()),
    path('api/search/category/<str:category>', views.SearchMusicCategoryView.as_view()),
]