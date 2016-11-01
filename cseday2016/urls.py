from django.conf.urls import url
from cseday2016 import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'[a-zA-Z]', views.index, name='index'),
<<<<<<< HEAD
        url(r'^message$',views.submit, name = 'submit'),
=======
        # url(r'^#$',views.submit, name = 'submit'),
>>>>>>> 06a32668951e2d175eccbbee19fa46f6e5853d91
        ]
