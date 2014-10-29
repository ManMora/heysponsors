from forms import UserCreateForm, ConcessionsCreateForm
from forms import EventReadForm, BenefitsCreateForm
from forms import EventCreateForm, NeedsCreateForm, SponsorshipCreateForm
from sponsorsManager.models import UserProfile, Benefit, Concession
from sponsorsManager.models import Event, Needs, Sponsorship
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
         url(r'^(?P<instance_id>\w{0,50})/events/add_event/$',
             views.general_create,
             {'generic_form': EventCreateForm,
              'template_name': 'sponsorsManager/event_create_form.html',
              'generic_model': Event,
              'auxiliar_id': -1
              },
             name='Add Event'),
         url(r'^(?P<user_name>\w{0,50})/edit/$',
             views.my_info, name='Edit user'),
         url(r'^(?P<user_name>\w{0,50})/history/$',
             views.history, name='history'),
         url(r'^events/(?P<instance_id>\w{0,50})$',
             views.general_groot,
             {
                 'generic_form': EventReadForm,
                 'template_name': "sponsorsManager/event_form.html",
                 'generic_model': Event,
             },
             name='events'),
         url(r'^events/(?P<instance_id>\w{0,50})/add_need/$',
             views.general_create,
             {
                 'generic_form': NeedsCreateForm,
                 'template_name': "sponsorsManager/need_create_form.html",
                 'generic_model': Needs,
                 'auxiliar_id': -1
             },
             name='events'),
         url(r'events/(?P<instance_id>\w{0,50})/needs/$',
             views.list_needs,
             name='needs'),
         url(r'events/(?P<instance_id>\w{0,50})/sponsorships/$',
             views.list_sponsorships,
             name='needs'),
         url(r'^needs/(?P<instance_id>\w{0,50})$',
             views.general_groot,
             {
                 'generic_form': NeedsCreateForm,
                 'template_name': "sponsorsManager/needs_form.html",
                 'generic_model': Needs,
             },
             name='needs'),
         url(r'^benefits/(?P<instance_id>\w{0,50})$',
             views.general_groot,
             {
                 'generic_form': BenefitsCreateForm,
                 'template_name': "sponsorsManager/stuff_from_sponsorship_form.html",
                 'generic_model': Benefit,
             },
             name='benefits'),
         url(r'^sponsorship/(?P<instance_id>\w{0,50})$',
             views.sponsorship,
             name='sponsorships'),
         url(r'^sponsorship/(?P<instance_id>\w{0,50})/delete$',
             views.delete_sponsorship,
             name='sponsorships'),
         url(r'^concession/(?P<instance_id>\w{0,50})$',
             views.general_groot,
             {
                 'generic_form': ConcessionsCreateForm,
                 'template_name': "sponsorsManager/stuff_from_sponsorship_form.html",
                 'generic_model': Concession,
             },
             name='concessions'),
         url(r'add_sponsorship/(?P<instance_id>\w{0,50})/(?P<auxiliar_id>\w{0,50})$',
            views.general_create,
            {
            'generic_model': Sponsorship,
            'generic_form': SponsorshipCreateForm,
            'template_name': 'sponsorsManager/sponsorship_create_form.html',
            })
         )