from django.conf.urls import *
from django.conf import settings

from selvbetjening.frontend.userportal import views as userportal_views

urlpatterns = patterns('',

    url(r'^$', 'selvbetjening.frontend.eventportal.views.events_list', name='home'),

    # user related

    (r'^auth/', include('selvbetjening.frontend.auth.urls')),

    url(r'^profil/medlemskab/$', 'kita_website.apps.kitamembership.views.profile_membershipstatus', name='kita_membership'),
    url(r'^profil/registration/$', userportal_views.register,
         kwargs={
             'login_on_success': True,
             'success_page': 'userportal_profile'
         },
         name='userportal_register'),
    url(r'^profil/update/$', userportal_views.edit_profile,
        name='userportal_edit_profile'),
    url(r'^profil/update/picture/$', userportal_views.edit_picture,
        name='userportal_edit_picture'),
    url(r'^profil/update/privacy/$', userportal_views.edit_privacy,
        name='userportal_edit_privacy'),
    url(r'^profil/update/password/$', userportal_views.edit_password,
        name='userportal_edit_password'),

    url(r'^profil/vis/(?P<username>[0-9a-zA-Z_\-]+)/$', userportal_views.public_profile_page,
        name='userportal_public_profile'),
    url(r'^profil/', userportal_views.profile, name='userportal_profile'),

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
