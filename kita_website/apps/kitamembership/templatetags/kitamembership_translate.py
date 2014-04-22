from django import template

from kita_website.apps.kitamembership.models import MembershipState, MembershipType

register = template.Library()


@register.filter(name='translate')
def translate(text, category):
    if category == 'membership_state':
        return MembershipState.get_display_name(text)

    if category == 'membership_state_short':
        return MembershipState.get_display_name_short(text)

    elif category == 'payment_type':
        return MembershipType.get_display_name(text)