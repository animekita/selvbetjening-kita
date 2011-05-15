from django.utils.translation import ugettext_lazy as _

from selvbetjening.core.selvadmin.admin import site

# initialize admin site
import selvbetjening.core.members.admin

# extend user admin
from django.contrib.auth.models import User
from selvbetjening.core.members.admin import UserAdminExt, UserProfileInline

from kita_website.apps.kitamembership.models import Membership, MembershipState
from kita_website.apps.kitamembership.admin import MembershipInline

class UserAdmin(UserAdminExt):
    def membership_status(instance):
        state = Membership.objects.get_membership_state(instance)
        return MembershipState.get_display_name_short(state)
    membership_status.short_description = 'Medlemskab'

    list_display = UserAdminExt.list_display + (membership_status,)

    inlines = UserAdminExt.inlines + [MembershipInline,]

site.replace(User, UserAdmin)

# continue initialization

import selvbetjening.core.events.admin
import selvbetjening.core.invoice.admin
import selvbetjening.core.logger.admin

import selvbetjening.core.mailcenter.admin

import selvbetjening.notify.concrete5.admin

import kita_website.apps.kitamembership.admin
import kita_website.apps.achievements.admin
