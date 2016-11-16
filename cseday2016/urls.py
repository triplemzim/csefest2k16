from django.conf.urls import url
from cseday2016 import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'[a-zA-Z]', views.index, name='index'),
        url(r'^message$',views.submit, name = 'submit'),

        ]
