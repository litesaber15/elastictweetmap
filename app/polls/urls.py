from django.conf.urls import url

from . import views

urlpatterns = [
            url(r'^$', views.index, name='index'),
            url('map', views.map, name='map'),
            url(r'ajax/getnewtweets$', views.livestream, name='livestream'),
            url(r'testfun', views.testfun, name='testfun')
            ]

