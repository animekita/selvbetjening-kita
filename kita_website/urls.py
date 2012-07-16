from django.conf.urls import *

from selvbetjening.portal.profile.views import profile_redirect
from selvbetjening.sadmin.base import sadmin

from kita_website.apps.kitamembership.views import profile_membershipstatus
from kita_website.apps.achievements.views import list_achievements

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# workaround for missing urls
from selvbetjening.sadmin.events import models as event_models
from selvbetjening.sadmin.mailcenter import models as mail_models
from selvbetjening.sadmin.members import models as members_models
from kita_website.apps.achievements import models as achievements_models

urlpatterns = patterns('',
    url(r'^$', profile_redirect, name='home'),

    url(r'^profil/medlemskab/', profile_membershipstatus, name='kita_membership'),
    url(r'^profil/achievements/', list_achievements, name='kita_list_achievements'),
    (r'^profil/opdater/forum/', include('selvbetjening.notify.vanillaforum.urls')),
    (r'^profil/', include('selvbetjening.portal.profile.urls')),

    (r'^bliv-medlem/', include('selvbetjening.portal.quickregistration.urls')),
    (r'^events/', include('selvbetjening.portal.eventregistration.urls')),

    (r'^sadmin/', include(sadmin.site.urls)),

    (r'^scheckin/legacy/', include('selvbetjening.scheckin.legacy.urls')),
)

urlpatterns += staticfiles_urlpatterns()