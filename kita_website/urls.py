from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to, direct_to_template

from selvbetjening.clients.profile.views import profile_redirect

from kita_website.apps.kitamembership.views import profile_membershipstatus
from kita_website import admin

urlpatterns = patterns('',
    url(r'^$', profile_redirect, name='home'),

    url(r'^profil/medlemskab/', profile_membershipstatus, name='kita_membership'),
    (r'^profil/', include('selvbetjening.clients.profile.urls')),

    (r'^bliv-medlem/', include('selvbetjening.clients.quickregistration.urls')),
    (r'^events/', include('selvbetjening.clients.eventregistration.urls')),

    (r'^admin/', include(admin.site.urls)),
)

if getattr(settings, 'STATIC_DEBUG', False):
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    )

