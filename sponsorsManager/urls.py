from django.conf.urls import patterns, url

from sponsorsManager import views

urlpatterns = patterns('',
    url(r'^login$', views.index, name='index'),
)