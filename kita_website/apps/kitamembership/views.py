from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from models import Membership


@login_required
def profile_membershipstatus(request,
                             template='kitamembership/profile/membershipstatus.html'):

    return render(request,
                  template,
                  {
                      'membership_status': Membership.objects.get_membership_state(request.user, datetime.today()),
                      'membership_passive_to': Membership.objects.passive_to(request.user),
                      'membership_to': Membership.objects.member_to(request.user),
                      'membership_date': Membership.objects.member_since(request.user),
                      'backlog': Membership.objects.get_recent_memberships(request.user, datetime.today())
                  })