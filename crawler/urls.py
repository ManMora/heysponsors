from django.conf.urls import patterns, url
from . import views


urlpatterns = patterns('',
    url(r'^$', views.testapi, name='crawler'),
    url(r'^gettags/$',views.gettags, name='crawler API test')
)
