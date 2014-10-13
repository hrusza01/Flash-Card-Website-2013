from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from epicstudy import settings

# Enable dajaxice
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'epicstudy.views.home', name='home'),
    url(r'^epicstudy/', include('flashcardapp.urls', namespace="flashcardapp")),
    url(r'^polls/', include('polls.urls', namespace="polls")),

    # Dajaxice
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
	
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'', include('social_auth.urls')),
    url(r'^logout/', 'flashcardapp.views.logout', {'next_page':settings.SOCIAL_AUTH_DISCONNECT_REDIRECT_URL}, name='logout'),
    url(r'^search/', include('haystack.urls')),
)

urlpatterns += staticfiles_urlpatterns()
