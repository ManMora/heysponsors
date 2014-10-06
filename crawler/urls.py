from django.conf.urls import patterns, url
from . import views


urlpatterns = patterns('',
    url(r'^gettags/$',views.gettags, name='crawler API test')
)
