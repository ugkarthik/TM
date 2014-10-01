from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from oscar.app import application

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'trendzmania.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^admin/', include(admin.site.urls)),

    url(r'^', include('tm.urls')),
    url(r'', include(application.urls)),
    
)

urlpatterns += staticfiles_urlpatterns()