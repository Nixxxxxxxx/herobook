from django.urls import re_path
from booktest import views

urlpatterns = [
    re_path(r'^heros/$', views.HeroListView.as_view()),
    re_path(r'^heros/(?P<id>\d+)/$', views.HeroDetaiView.as_view())
]