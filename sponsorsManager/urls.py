from forms import UserCreateForm
from forms import EventReadForm
from forms import EventCreateForm
from sponsorsManager.models import UserProfile
from sponsorsManager.models import Event
from django.conf.urls import patterns, url
from sponsorsManager import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^auth/$', views.auth_view),
    url(r'^invalid/$', views.invalid, name='index'),
    url(r'^signup/$', 
    	views.signup, 
    	name='signup'),
    url(r'^(?P<petition>\w{0,50})/$', 
    	views.main_controller, 
    	name='index'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^events/add_event/$',
    	views.general_create,
    	{'generic_form': EventCreateForm,
    	'template_name': 'sponsorsManager/event_create_form.html'
    	},
    	 name='Add Event'),
    url(r'^(?P<user_name>\w{0,50})/edit/$',
        views.groot_user, name='Edit user'),
    url(r'^(?P<user_name>\w{0,50})/events/$',
        views.event_view, name='events'),
    url(r'^(?P<user_name>\w{0,50})/events/(?P<instance_id>\w{0,50})$',
        views.general_groot, 
        {
        'generic_form': EventReadForm,
        'template_name': "sponsorsManager/event_form.html",
        'generic_model': Event,
        },
        name='events'),

)