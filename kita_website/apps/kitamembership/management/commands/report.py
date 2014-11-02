# ==encoding: utf-8 ==

from datetime import date, timedelta
import codecs

from django.core.management.base import BaseCommand, CommandError

from kita_website.apps.kitamembership.models import Membership, MembershipState, MembershipType
from selvbetjening.core.user.models import SUser

class Command(BaseCommand):
    args = '<year>'
    help = 'Generates a yearly report for all membership activity'

    def handle(self, year, *args, **options):

        members = {}

        if year == 'now':
            at_date = date.today()
            bf_date = at_date - timedelta(days=356)
        else:
            at_date = date(int(year), 12, 31)
            bf_date = date(int(year)-1, 12, 31)

        fp = codecs.open("report-%s.txt" % year, "w", "utf-8")

        membership_income = 0
        for membership in Membership.objects.filter(bind_date__lt=at_date).filter(bind_date__gt=bf_date).select_related():
            if membership.attendee.is_paid():
                membership_income += membership.price

        fp.write(u'=============\n')
        fp.write(u'Medlemskab indtægt %s DKK\n' % membership_income)
        fp.write(u'=============\n')

        for user in SUser.objects.all():
            state = Membership.objects.get_membership_state(user, at_date)

            if state != MembershipState.INACTIVE and state != MembershipState.PASSIVE:
                age = user.get_age()
                members[age] = members.get(age, [])
                members[age].append((user, state))

        ranges = [range(0, 7), range(7, 18), range(18, 25), range(25, 120)]

        for r in ranges:

            fp.write(u'\n')
            fp.write(u'=============\n')
            fp.write(u'Fra %s til %s\n' % (r[0], r[-1]))

            count = 0
            for age in r:
                for user in members.get(age, []):
                    count += 1

            fp.write(u'%s medlemmer i alt\n' % count)
            fp.write(u'=============\n')

            for age in r:
                for user, state in members.get(age, []):

                    fp.write('\n')
                    fp.write(u'%s %s\n' % (user.first_name, user.last_name))
                    fp.write(u'%s\n' % user.dateofbirth)
                    fp.write(u'%s %s %s\n' % (user.street, user.city, user.postalcode))


                    memberships = []
                    for membership in Membership.objects.filter(user=user).filter(bind_date__lt=at_date).order_by('-bind_date'):
                        if membership.attendee.is_paid():
                            memberships.append(membership)

                    def print_memberships(ms):
                        for m in ms:
                            fp.write('%s %s\n' % (m.bind_date, MembershipType.get_display_name(m.membership_type)))

                    if memberships[0].membership_type == 'SRATE':
                        print_memberships(memberships[:2])
                    else:
                        print_memberships(memberships[:1])

        fp.close()






