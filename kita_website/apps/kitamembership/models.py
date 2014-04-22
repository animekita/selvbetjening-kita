from datetime import datetime, timedelta

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from selvbetjening.core.events.models import Attend


class MembershipState(object):
    INACTIVE = 'INACTIVE'
    PASSIVE = 'PASSIVE'
    CONDITIONAL_ACTIVE = 'CONDITIONAL_ACTIVE'
    ACTIVE = 'ACTIVE'

    @staticmethod
    def get_display_name(membership_state):
        names = {'INACTIVE': _('Inactive member'),
                 'PASSIVE': _('Passive member'),
                 'CONDITIONAL_ACTIVE': _('Conditional active member'),
                 'ACTIVE': _('Active member')}

        return unicode(names.get(membership_state, membership_state))

    @staticmethod
    def get_display_name_short(membership_state):
        names = {'INACTIVE': _('Inactive'),
                 'PASSIVE': _('Passive'),
                 'CONDITIONAL_ACTIVE': _('Conditional active'),
                 'ACTIVE': _('Active')}

        return unicode(names.get(membership_state, membership_state))


class MembershipType(object):
    FULL = 'FULL'
    FRATE = 'FRATE'
    SRATE = 'SRATE'

    NONE = 'NONE'

    names = {'FULL': _('Full payment'),
             'FRATE': _('First rate'),
             'SRATE': _('Second rate'),
             'NONE': _('No membership payment')}

    @classmethod
    def get_display_name(cls, membership_type):

        return unicode(cls.names.get(membership_type, membership_type))


class MembershipManager(models.Manager):

    def get_recent_memberships(self, user, at_date,
                               fake_attendance_paid=None):

        memberships = []
        for membership in Membership.objects\
                .filter(user=user)\
                .filter(bind_date__lte=at_date)\
                .order_by('-bind_date')\
                .select_related():

            if membership.attendee.is_paid() or membership.attendee == fake_attendance_paid:
                memberships.append(membership)

        return memberships

    def get_membership_state(self, user, at_date,
                             fake_upgrade_attendance_as_full=None,
                             fake_attendance_paid=None):

        memberships = self.get_recent_memberships(user, at_date, fake_attendance_paid)

        if len(memberships) == 0:
            return MembershipState.INACTIVE

        if memberships[0].membership_type == 'SRATE':
            last = memberships[1]
        else:
            last = memberships[0]

        payment_quater = self.total_quaters(last.bind_date)
        now_quater = self.total_quaters(at_date)

        if payment_quater + 8 <= now_quater:
            return MembershipState.INACTIVE
        elif payment_quater + 4 <= now_quater:
            return MembershipState.PASSIVE
        elif memberships[0].membership_type == 'FULL' or \
                memberships[0].membership_type == 'SRATE' or\
                memberships[0].attend == fake_upgrade_attendance_as_full:

            return MembershipState.ACTIVE
        else:
            return MembershipState.CONDITIONAL_ACTIVE

    def get_membership_choices(self, user, event):

        state = self.get_membership_state(user, event.startdate - timedelta(days=1))

        if state == MembershipState.ACTIVE:
            return []
        elif state == MembershipState.CONDITIONAL_ACTIVE:
            return [MembershipType.SRATE]
        else:
            return [MembershipType.FULL,
                    MembershipType.FRATE]

    def select_membership(self, attendee, membership_type):

        membership, created = Membership.objects.get_or_create(
            user=attendee.user,
            bind_date=attendee.event.startdate,
            attendee=attendee,
            defaults={
                'membership_type': membership_type
            })

        if not created and membership.membership_type != membership_type:
            membership.membership_type = membership_type
            membership.save()

    def last_member_period(self, user):
        """ Returns the timestamp marking the beginning of the last user membership period """

        memberships = self.get_recent_memberships(user, datetime.today())

        if len(memberships) == 0:
            return None

        if memberships[0].membership_type == 'SRATE':
            return memberships[1].bind_date
        else:
            return memberships[0].bind_date

    def member_since(self, user):

        last_payment_timestamp = self.last_member_period(user)

        if last_payment_timestamp is None:
            return None

        payment_quater = self.total_quaters(last_payment_timestamp)

        if payment_quater + 4 <= self.total_quaters(datetime.now()):
            return None
        else:
            return last_payment_timestamp

    def member_to(self, user):

        timestamp = self.member_since(user)

        if timestamp is not None:
            year = timestamp.year + 1
            month = (self.to_quarter(timestamp) - 1) * 3 + 1
            return datetime(year, month, 1).date() - timedelta(days=1)
        else:
            return None

    def passive_to(self, user):

        last_payment_timestamp = self.last_member_period(user)

        if last_payment_timestamp is not None:
            year = last_payment_timestamp.year + 2
            month = (self.to_quarter(last_payment_timestamp) - 1) * 3 + 1
            return datetime(year, month, 1).date() - timedelta(days=1)
        else:
            return None

    def to_quarter(self, date):
        return ((date.month-1) / 3) + 1

    def total_quaters(self, timestamp):
        return timestamp.year * 4 + self.to_quarter(timestamp)


class Membership(models.Model):
    """
    Two types of payments can be used, full (one time) payment or rate
    (divided into two rates) payment.

    The first rate of the rate payment method is paied at a specific event,
    and the second payment must be paied at the second event. The timestamp
    is used to determine which event the payment is associated to.

    The system assumes that membership sequences are proper. That is, SRATE is
    always after a FRATE. Memberships related to unpaid attendees are ignored.

    It is only possible to relate a membership to an attendee at an event. Events
    are used as fixed points in time were memberships are attached and selected.

    We assume that events are not moved in time (startdate is fixed).

    It is a known problem that memberships can be added for event B (and paid for),
    but this is not visible when membership status is selected for event A were A
    happens before B. In this case, we expect the membership to be added to A as usual,
    and manually changed/canceled for B.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(u'user'))
    attendee = models.ForeignKey(Attend)

    bind_date = models.DateTimeField()
    membership_type = models.CharField(max_length=5, choices=[(key, MembershipType.get_display_name(key)) for key in MembershipType.names])

    objects = MembershipManager()

    @property
    def price(self):
        try:
            yearly_rate = YearlyRate.objects.get(year=self.bind_date.year)
            rate = yearly_rate.rate
        except YearlyRate.DoesNotExist:
            rate = 0

        if self.membership_type == 'FULL':
            return rate
        else:
            return rate / 2

    def __unicode__(self):
        return unicode(MembershipType.get_display_name(self.membership_type))


class YearlyRate(models.Model):
    year = models.IntegerField(max_length=4)
    rate = models.DecimalField(max_digits=6, decimal_places=2)

    def __unicode__(self):
        return _(u"Yearly rate for %s") % self.year

