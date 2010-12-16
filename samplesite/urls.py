import django.contrib.auth.views

from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'samplesite.sampleapp.views.home' ),
    (r'^download/(?P<id>\d+)/$', 'samplesite.sampleapp.views.download' ), # view a purchase
    (r'^purchased/(?P<uid>\d+)/(?P<id>\d+)/$', 'samplesite.sampleapp.views.purchased' ), # purchase callback

    # authentication
    (r'^accounts/$', 'django.contrib.auth.views.login'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    (r'^accounts/profile/$', 'samplesite.sampleapp.views.profile'),

    (r'^admin/', include(admin.site.urls)),
)
