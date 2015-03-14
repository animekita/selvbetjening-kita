from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from models import Membership
from selvbetjening.core.user.models import SUser
from selvbetjening.sadmin2 import menu
from selvbetjening.sadmin2.decorators import sadmin_prerequisites


@login_required
def profile_membershipstatus(request,
                             template='kitamembership/profile/membershipstatus.html'):

    return render(request,
                  template,
                  {
                      'membership_status': Membership.objects.get_membership_state(request.user, datetime.today()),
                      'membership_to': Membership.objects.member_to(request.user),
                      'membership_date': Membership.objects.member_since(request.user),
                      'backlog': Membership.objects.get_recent_memberships(request.user, datetime.today())
                  })


@sadmin_prerequisites
def sadmin2_membershipstatus(request, user_pk):

    user = get_object_or_404(SUser, pk=user_pk)
    memberships = Membership.objects.filter(user=user).order_by('-pk')
    membership_state = Membership.objects.get_membership_state(user, datetime.today())

    return render(request, 'sadmin2/user/membership.html',
                  {
                      'sadmin2_menu_main_active': 'userportal',
                      'sadmin2_breadcrumbs_active': 'user_membership',
                      'sadmin2_menu_tab': menu.sadmin2_menu_tab_user,
                      'sadmin2_menu_tab_active': 'membership',

                      'user': user,
                      'memberships': memberships,
                      'membership_state': membership_state
                  })