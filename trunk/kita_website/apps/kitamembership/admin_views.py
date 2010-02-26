from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from models import Membership, MembershipState

@staff_member_required
def membership_statistics(request,
                          model_admin,
                          template_name='admin/kitamembership/membership/statistics.html'):

    if not model_admin.has_change_permission(request, None):
        raise PermissionDenied

    active = 0
    conditional_active = 0
    passive = 0
    inactive = 0

    for user in User.objects.all():
        state = Membership.objects.get_membership_state(user)

        if state == MembershipState.ACTIVE:
            active += 1
        elif state == MembershipState.CONDITIONAL_ACTIVE:
            conditional_active += 1
        elif state == MembershipState.PASSIVE:
            passive += 1
        else:
            inactive += 1

    return render_to_response(template_name,
                              {'active': active,
                               'conditional_active' : conditional_active,
                               'passive' : passive,
                               'inactive': inactive,
                               'total' : active + conditional_active + passive},
                              context_instance=RequestContext(request))
