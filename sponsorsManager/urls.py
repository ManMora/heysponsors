from forms import UserCreateForm
from forms import EventCreateForm
from django.conf.urls import patterns, url
from sponsorsManager import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^auth/$', views.auth_view),
    url(r'^invalid/$', views.invalid, name='index'),
    url(r'^signup/$', 
    	views.general_create, 
    	{'generic_form':UserCreateForm,
    	'template_name':'sponsorsManager/signup.html'
    	},
    	name='signup'),
    url(r'^(?P<petition>\w{0,50})/$', 
    	views.main_controller, 
    	name='index'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^events/add_event/$',
    	views.general_create,
    	{'generic_form': EventCreateForm,
    	'template_name': 'sponsorsManager/event_form.html'
    	},
    	 name='Add Event'),

)