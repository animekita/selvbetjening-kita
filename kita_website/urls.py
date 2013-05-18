from django.conf.urls import *

from selvbetjening.portal.profile.views import profile_redirect
from selvbetjening.sadmin.base import sadmin

from kita_website.apps.kitamembership.views import profile_membershipstatus
from kita_website.apps.achievements.views import list_achievements

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from selvbetjening.sadmin.members.models import MembersRootAdmin
from selvbetjening.sadmin.events.models import EventsRootAdmin
from selvbetjening.sadmin.mailcenter.models import MailcenterRootAdmin

sadmin.site.register('members', MembersRootAdmin)
sadmin.site.register('events', EventsRootAdmin)
sadmin.site.register('mailcenter', MailcenterRootAdmin)

from kita_website.apps.achievements.models import PositionAdmin

sadmin.site.register('achievements', PositionAdmin)

from kita_website.apps.webfactionemail.admin import EmailAdmin

sadmin.site.register('webfaction', EmailAdmin)

from kita_website.apps.kitamembership.admin import MembershipAdmin

sadmin.site.register('kita/membership', MembershipAdmin)

urlpatterns = patterns('',
    url(r'^$', profile_redirect, name='home'),

    url(r'^profil/medlemskab/', profile_membershipstatus, name='kita_membership'),
    url(r'^profil/achievements/', list_achievements, name='kita_list_achievements'),
    (r'^profil/opdater/forum/', include('selvbetjening.notify.vanillaforum.urls')),
    (r'^profil/', include('selvbetjening.portal.profile.urls')),

    (r'^bliv-medlem/', include('selvbetjening.portal.quickregistration.urls')),
    (r'^events/', include('selvbetjening.portal.eventregistration.urls')),

    (r'^sadmin/', include(sadmin.site.urls)),

    (r'^api/rest/', include('selvbetjening.api.rest.urls')),
    (r'^api/sso/', include('selvbetjening.api.sso.urls')),
    (r'^scheckin/', include('selvbetjening.scheckin.urls')),

)

urlpatterns += staticfiles_urlpatterns()
