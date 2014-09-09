from django.conf.urls import patterns, url
from sponsorsManager import views

urlpatterns = patterns('',
	url(r'^login$', views.login, name='index'),
    url(r'^$', views.login, name='index'),
)