from django.urls import re_path
from booktest import views

urlpatterns = [
    re_path(r'^herolist/$', views.HeroListView.as_view()),
    re_path(r'^herodetai/(?P<id>\d+)/$', views.HeroDetaiView.as_view())
]