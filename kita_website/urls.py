from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to, direct_to_template

from selvbetjening.portal.profile.views import profile_redirect
from selvbetjening.sadmin.base import sadmin

from kita_website.apps.kitamembership.views import profile_membershipstatus
from kita_website.apps.achivements.views import list_achivements
from kita_website import admin

urlpatterns = patterns('',
    url(r'^$', profile_redirect, name='home'),


    url(r'^profil/medlemskab/', profile_membershipstatus, name='kita_membership'),
    url(r'^profil/achievements/', list_achivements, name='kita_list_achivements'),
    (r'^profil/', include('selvbetjening.portal.profile.urls')),

    (r'^bliv-medlem/', include('selvbetjening.portal.quickregistration.urls')),
    (r'^events/', include('selvbetjening.portal.eventregistration.urls')),

    (r'^admin/', include(admin.site.urls)),
    (r'^sadmin/', include(sadmin.site.urls)),
)

if getattr(settings, 'STATIC_DEBUG', False):
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    )

