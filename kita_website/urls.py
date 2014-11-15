from django.conf.urls import *
from django.conf import settings

urlpatterns = patterns('',

    url(r'^$', 'selvbetjening.frontend.eventportal.views.events_list', name='home'),

    # user related

    (r'^auth/', include('selvbetjening.frontend.auth.urls')),

    url(r'^profil/medlemskab/$', 'kita_website.apps.kitamembership.views.profile_membershipstatus', name='kita_membership'),
    (r'^profil/', include('selvbetjening.frontend.userportal.urls')),

    # event related

    (r'^events/', include('selvbetjening.frontend.eventsingle.urls')),
    (r'^events/', include('selvbetjening.frontend.eventportal.urls')),

    # /sadmin2/

    url(r'^sadmin2/users/(?P<user_pk>[0-9a-zA-Z_\-]+)/membership/$',
        'kita_website.apps.kitamembership.views.sadmin2_membershipstatus',
        name='kita_membership_sadmin2'),
    (r'^%s/' % settings.SADMIN2_BASE_URL, include('selvbetjening.sadmin2.urls', namespace='sadmin2')),

    # /api/

    (r'^api/rest/', include('selvbetjening.api.rest.urls')),
    (r'^api/sso/', include('selvbetjening.api.sso.urls')),
    (r'^api/jsconnect/', include('pyjsconnect.django.urls'))
                       
)

if getattr(settings, 'STATIC_DEBUG', False):
    urlpatterns += patterns(
        '',
        (r'^%s(?P<path>.*)$' % settings.STATIC_URL, 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}))
