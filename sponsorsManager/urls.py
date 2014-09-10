from django.conf.urls import patterns, url
from sponsorsManager import views

urlpatterns = patterns('',
    url(r'^$', views.login, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^auth/$', views.auth_view),
    url(r'^index/$', views.index, name='index'),
    url(r'^invalid/$', views.invalid, name='index'),
    url(r'^signup/$', views.signup_form, name='signup'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^add_event/$', views.create_event, name='Add Event'),

)