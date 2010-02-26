from django.shortcuts import render_to_response
from django.template import RequestContext

from models import Membership

def profile_membershipstatus(request,
                             template='kitamembership/profile/membershipstatus.html'):
    data = {'membership_status' : Membership.objects.get_membership_state(request.user),
            'membership_passive_to' : Membership.objects.passive_to(request.user),
            'membership_to' : Membership.objects.member_to(request.user),
            'membership_date' : Membership.objects.member_since(request.user)}

    return render_to_response(template,
                              data,
                              context_instance=RequestContext(request))