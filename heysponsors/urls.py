# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'heysponsors.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('sponsorsManager.urls')),
	url(r'^sponsors/', include('sponsorsManager.urls')),
	url(r'^crawler/', include('crawler.urls')),

)
