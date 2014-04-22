from datetime import datetime
from django import template
from django.utils.translation import ugettext as _

from kita_website.apps.kitamembership.models import Membership
import kitamembership_translate

register = template.Library()


@register.filter(name='membership_state')
def membership_state(user):
    state = Membership.objects.get_membership_state(user, datetime.today())
    return kitamembership_translate.translate(state, 'membership_state')