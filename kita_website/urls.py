from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to, direct_to_template
from django.core.urlresolvers import reverse
from selvbetjening.portal.profile.views import profile_redirect
from selvbetjening.sadmin.base import sadmin

from kita_website.apps.kitamembership.views import profile_membershipstatus
from kita_website.apps.achievements.views import list_achievements

# workaround for missing urls
from selvbetjening.sadmin.events import models as event_models
from selvbetjening.sadmin.mailcenter import models as mail_models
from selvbetjening.sadmin.members import models as members_models
from kita_website.apps.achievements import models as achievements_models
from kita_website.apps.comicparty import models as comicparty_models

urlpatterns = patterns('',
    url(r'^$', profile_redirect, name='home'),

    url(r'^profil/medlemskab/', profile_membershipstatus, name='kita_membership'),
    url(r'^profil/achievements/', list_achievements, name='kita_list_achievements'),
    (r'^profil/', include('selvbetjening.portal.profile.urls')),

    (r'^bliv-medlem/', include('selvbetjening.portal.quickregistration.urls')),
    (r'^events/', include('selvbetjening.portal.eventregistration.urls')),

    (r'^tilbud/comic-party/', include('kita_website.apps.comicparty.urls')),

    (r'^sadmin/', include(sadmin.site.urls)),
)

if getattr(settings, 'STATIC_DEBUG', False):
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    )

