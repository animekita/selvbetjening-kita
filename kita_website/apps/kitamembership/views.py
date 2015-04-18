# ==encoding: utf-8 ==
from collections import defaultdict

import re
import itertools
from datetime import datetime, date, timedelta
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from models import Membership, MembershipState
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


@sadmin_prerequisites
def sadmin2_membership_report(request):

    def parse_date(input):
        try:
            match = re.match('([0-9]+)/([0-9]+)/([0-9]+)', input)

            month = match.group(1)
            day = match.group(2)
            year = match.group(3)

            return date(int(year), int(month), int(day))
        except:
            return date.today()

    at_date = parse_date(request.GET.get('to')) if request.GET.get('to', None) else date.today()
    bf_date = parse_date(request.GET.get('from')) if request.GET.get('from', None) else date.today() - timedelta(days=356)

    full = request.GET.get('full', 'on') == 'on'

    total_income, report = _get_report(at_date, bf_date, full)

    return render(request, 'sadmin2/users/membershipreport.html',
                  {
                      'sadmin2_menu_main_active': 'userportal',
                      'sadmin2_breadcrumbs_active': 'user_membershipreport',
                      'sadmin2_menu_tab': menu.sadmin2_menu_tab_users,
                      'sadmin2_menu_tab_active': 'reports',

                      'at_date': at_date,
                      'bf_date': bf_date,

                      'total_income': total_income,
                      'report': report
                  })


def _get_report(at_date, bf_date, show_members_without_payments):
    """
    Returns (total_income, [(range_start_age, range_end_age, [
                               (user, state, [membership])
                           ]]
    :param year:
    :return:
    """

    bf2x_date = bf_date - timedelta(days=356)

    members = defaultdict(list)
    membership_income = 0

    # Calculate membership income in period

    for membership in Membership.objects.filter(bind_date__lte=at_date).filter(bind_date__gt=bf_date).select_related():
        if membership.attendee.is_paid():
            membership_income += membership.price

    # Create list of non-inactive members + state + membership payments in period

    for user in SUser.objects.filter(membership__bind_date__lte=at_date,
                                     membership__bind_date__gt=bf2x_date).distinct().select_related().prefetch_related('membership_set'):
        # iterate  over all members who have memberships within the period or one  year before the period
        # this should restrict us to the subset of users who are still active

        state = Membership.objects.get_membership_state(user, at_date)

        if state != MembershipState.INACTIVE:
            age = user.get_age()

            memberships = []
            for membership in user.membership_set.filter(bind_date__lte=at_date,
                                                         bind_date__gt=bf_date).order_by('-bind_date').select_related():
                if membership.attendee.is_paid():
                    memberships.append(membership)

            if show_members_without_payments or len(memberships) > 0:
                members[age].append((user, state, memberships))

    ranges = [range(0, 7), range(7, 18), range(18, 25), range(25, 120)]
    output = []
    for r in ranges:
        output.append((r[0], r[-1], list(itertools.chain(*[members.get(age, []) for age in r]))))

    return membership_income, output
