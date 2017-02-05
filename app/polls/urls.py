from django.conf.urls import url

from . import views

urlpatterns = [
            url(r'^$', views.index, name='index'),
            url('map', views.map, name='map'),
            url(r'ajax/getnewtweets$', views.livestream, name='livestream'),
            url(r'testfun', views.testfun, name='testfun'),
            url(r'submit', views.submit, name='submit'),
            url(r'download/(?P<file>.*)/$', views.download, name='download'),
            url(r'download_zip/(?P<fnames>.*)/$', views.download_zip, name='download_zip'),
            ]

