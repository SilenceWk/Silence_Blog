from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^(?P<pageid>[0-9]+)/$', views.index, name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category'),
    url(r'^createqrcode/$', views.createQR, name='createqrcode'),
    url(r'^QRinput/$', views.QRinput, name='QRinput'),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView, name='tag'),
    # url(r'^search/$', views.search, name='search'),

]
