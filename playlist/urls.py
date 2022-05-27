from django.urls import path
from . import views

app_name = "playlist"

urlpatterns = [
  path('', views.ManagePlaylist.as_view()),
  path('all/', views.GetPlaylistAll.as_view()),
]
