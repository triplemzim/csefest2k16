from django.conf import settings
# from django.conf.urls.static import static

"""testsharethis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import include, url

from django.conf.urls.static import static
from . import views

app_name='picturepuzzle'

urlpatterns = [
    
    
    url(r'^$', views.index , name = 'index'),
    url(r'^login$', views.Login , name = 'Login'),
    url(r'^logout$', views.Logout , name = 'Logout'),
    url(r'^signup$', views.Signup , name = 'Signup'),
    url(r'^leaderboard$', views.Leaderboard , name = 'Leaderboard'),

    

]
        

