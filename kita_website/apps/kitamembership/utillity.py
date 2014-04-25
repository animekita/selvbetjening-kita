from datetime import datetime
from django.contrib.auth.models import User

from kita_website.apps.kitamembership.models import Membership, MembershipState


def get_membership_statistics(max_age_inclusive=None):
    active = 0
    conditional_active = 0
    passive = 0
    inactive = 0

    for user in User.objects.all():
        profile = user.get_profile()

        if max_age_inclusive is not None and \
           profile.get_age() > max_age_inclusive:
            continue

        state = Membership.objects.get_membership_state(user, datetime.today())

        if state == MembershipState.ACTIVE:
            active += 1
        elif state == MembershipState.CONDITIONAL_ACTIVE:
            conditional_active += 1
        elif state == MembershipState.PASSIVE:
            passive += 1
        else:
            inactive += 1

    return {'active': active,
            'conditional_active' : conditional_active,
            'passive' : passive,
            'inactive': inactive,
            'total' : active + conditional_active + passive}