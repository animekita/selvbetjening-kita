from django.conf.urls import *
from django.conf import settings

#from selvbetjening.portal.profile.views import profile_redirect

urlpatterns = patterns('',

    url(r'^$', 'selvbetjening.frontend.eventportal.views.events_list', name='home'),



    #url(r'^profil/medlemskab/', profile_membershipstatus, name='kita_membership'),
    #url(r'^profil/achievements/', list_achievements, name='kita_list_achievements'),
    #(r'^profil/opdater/forum/', include('selvbetjening.notify.vanillaforum.urls')),
    #(r'^profil/', include('selvbetjening.portal.profile.urls')),

    (r'^auth/', include('selvbetjening.frontend.auth.urls')),
    (r'^profile/', include('selvbetjening.frontend.userportal.urls')),
    #(r'^events/', include('selvbetjening.portal.eventregistration.urls')),

    # /sadmin2/
    (r'^%s/' % settings.SADMIN2_BASE_URL, include('selvbetjening.sadmin2.urls', namespace='sadmin2')),

    # /api/
    (r'^api/rest/', include('selvbetjening.api.rest.urls')),
    (r'^api/sso/', include('selvbetjening.api.sso.urls'))

)

if getattr(settings, 'STATIC_DEBUG', False):
    urlpatterns += patterns(
        '',
        (r'^%s(?P<path>.*)$' % settings.STATIC_URL, 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}))
