from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.home),
    url(r'^preprocess/(?P<review>.+)', views.preprocess),
    url(r'^1/(?P<id>\d+)/(?P<sentence>.+)', views.subjectivity),
    url(r'^2/(?P<id>\d+)/(?P<sentence>.+)', views.clues),
    url(r'^3/(?P<clue>\w)/(?P<id>\d+)/(?P<sentence>.+)', views.sentiment),
    url(r'^4/(?P<functional>.+)/(?P<humanic>.+)/(?P<mechanic>.+)/(?P<general>.+)', views.overall),
    url(r'^presentation$', views.presentation),
    url(r'^presentation/1$', views.presentation1),
    url(r'^presentation/2$', views.presentation2),
    url(r'^presentation/3$', views.presentation3),
)
