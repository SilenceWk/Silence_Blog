from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^comment/post/(?P<post_pk>[0-9]+)$', views.post_comment, name='post_comment'),
]
