from django.conf.urls import patterns, url
from cseday2016 import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'[a-zA-Z]', views.index, name='index'),
        ]
