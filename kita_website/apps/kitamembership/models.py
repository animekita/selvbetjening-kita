from datetime import datetime, timedelta

from django.db import models
from django.db.models import F
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from selvbetjening.core.events.models import Attend, Option, Selection, AttendeeComment
from selvbetjening.core.events import options
from selvbetjening import sadmin2
from selvbetjening.core.events.options.scope import SCOPE
from selvbetjening.core.events.options.typemanager import ChoiceTypeManager
from selvbetjening.core.events.options.widgets import ChoiceWidget
from selvbetjening.core.events.signals import attendee_updated_signal
from selvbetjening.sadmin2 import menu
from selvbetjening.sadmin2.options.forms import option_form_factory
from selvbetjening.sadmin2.options.stypemanager import SBaseTypeManager

MEMBERSHIP_OPTION_TYPE_ID = 'kitamembership'
MEMBERSHIP_NOPASS_OPTION_TYPE_ID = 'kitamembershipnopass'
MEMBERSHIP_OPTION_TYPE_IDS = (MEMBERSHIP_OPTION_TYPE_ID, MEMBERSHIP_NOPASS_OPTION_TYPE_ID)


class MembershipState(object):
    INACTIVE = 'INACTIVE'
    CONDITIONAL_ACTIVE = 'CONDITIONAL_ACTIVE'
    ACTIVE = 'ACTIVE'

    @staticmethod
    def get_display_name(membership_state):
        names = {'INACTIVE': _('Inactive member'),
                 'CONDITIONAL_ACTIVE': _('Conditional active member'),
                 'ACTIVE': _('Active member')}

        return unicode(names.get(membership_state, membership_state))

    @staticmethod
    def get_display_name_short(membership_state):
        names = {'INACTIVE': _('Inactive'),
                 'CONDITIONAL_ACTIVE': _('Conditional active'),
                 'ACTIVE': _('Active')}

        return unicode(names.get(membership_state, membership_state))


class MembershipType(object):

    # old generation

    FULL = 'FULL'
    FRATE = 'FRATE'
    SRATE = 'SRATE'

    # new generation

    RATE = 'RATE'
    PASS = 'PASS'

    NONE = 'NONE'

    names = {'FULL': _('Full payment'),
             'FRATE': _('First rate'),
             'SRATE': _('Second rate'),
             'RATE': _('Membership'),
             'PASS': _('One time pass'),
             'NONE': _('No membership payment')}

    @classmethod
    def get_display_name(cls, membership_type):
        return unicode(cls.names.get(membership_type, membership_type))

    @classmethod
    def reverse(cls, label):
        """
         My eyes!
        """
        for key, name in cls.names.items():
            if name == label:
                return key

        raise ValueError


_membership_prices = {
    MembershipType.FULL: 100,
    MembershipType.SRATE: 50,
    MembershipType.FRATE: 50,
    MembershipType.RATE: 150,
    MembershipType.PASS: 0
}


class MembershipManager(models.Manager):

    def get_recent_memberships(self, user, at_date, fake_attendance_paid=None):

        memberships = []
        for membership in user.membership_set\
                .filter(bind_date__lte=at_date)\
                .order_by('-bind_date')\
                .select_related():

            if membership.attendee.is_paid() or membership.attendee == fake_attendance_paid:
                memberships.append(membership)

        return memberships

    def get_membership_state(self, user, at_date,
                             fake_upgrade_attendance_as_full=None,
                             fake_attendance_paid=None):

        if fake_upgrade_attendance_as_full is not None:
            fake_upgrade_attendance_as_full = fake_upgrade_attendance_as_full.pk

        memberships = self.get_recent_memberships(user, at_date, fake_attendance_paid)

        if len(memberships) == 0:
            return MembershipState.INACTIVE

        if memberships[0].membership_type == 'SRATE':
            if len(memberships) > 1:
                last = memberships[1]
            else:
                return MembershipState.INACTIVE
        else:
            # Handle FRATE/FULL/RATE/PASS cases
            last = memberships[0]

        payment_quater = self.total_quaters(last.bind_date)
        now_quater = self.total_quaters(at_date)

        if payment_quater + 4 <= now_quater:
            return MembershipState.INACTIVE
        elif memberships[0].membership_type in [MembershipType.FULL,
                                                MembershipType.SRATE,
                                                MembershipType.RATE]:
            return MembershipState.ACTIVE
        elif memberships[0].attendee.pk == fake_upgrade_attendance_as_full:
            # allow FRATE and PASS cases to count as full membership for this specific event
            return MembershipState.ACTIVE
        elif memberships[0].membership_type == MembershipType.FRATE:
            return MembershipState.CONDITIONAL_ACTIVE
        else:
            return MembershipState.INACTIVE  # PASS case

    def get_membership_choices(self, user, event, allow_pass=True):

        state = self.get_membership_state(user, event.startdate - timedelta(days=1))

        if state == MembershipState.ACTIVE:
            return []
        elif state == MembershipState.CONDITIONAL_ACTIVE:
            return [MembershipType.SRATE]
        else:
            if allow_pass:
                num_memberships = Membership.objects.filter(user=user).filter(
                    attendee__paid__gte=F('attendee__price')).count()

                if num_memberships == 0:
                    return [MembershipType.RATE, MembershipType.PASS]

            return [MembershipType.RATE]

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
        elif memberships[0].membership_type == 'PASS':
            return None
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

    def to_quarter(self, date):
        return ((date.month-1) / 3) + 1

    def total_quaters(self, timestamp):
        return timestamp.year * 4 + self.to_quarter(timestamp)

    def get_membership_price(self, membership_type):
        return _membership_prices[membership_type]


class Membership(models.Model):
    """

    OLD STYLE
    =========

    Two types of payments can be used, full (one time) payment or rate
    (divided into two rates) payment.

    The first rate of the rate payment method is paied at a specific event,
    and the second payment must be paied at the second event. The timestamp
    is used to determine which event the payment is associated to.

    The system assumes that membership sequences are proper. That is, SRATE is
    always after a FRATE. Memberships related to unpaid attendees are ignored.

    NEW  STYLE
    ==========

    Two types of payments can be used, full (one time) payment (RATE) or a free
    one-time membership for a single event (PASS). A pass may only be used once
    and only at specific events.

    LIMITATIONS
    ===========

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

    bind_date = models.DateField()
    membership_type = models.CharField(max_length=5, choices=[(key, MembershipType.get_display_name(key))
                                                              for key in MembershipType.names])

    objects = MembershipManager()

    @property
    def price(self):
        return Membership.objects.get_membership_price(self.membership_type)

    def __unicode__(self):
        return unicode(MembershipType.get_display_name(self.membership_type))


### Signal handling

@receiver(post_delete, sender=Selection)
def selection_delete_handler(sender, **kwargs):
    instance = kwargs['instance']

    if instance.option.type in MEMBERSHIP_OPTION_TYPE_IDS:
        Membership.objects.filter(attendee=instance.attendee).delete()


@receiver(post_save, sender=Selection)
def selection_save_handler(sender, **kwargs):
    instance = kwargs['instance']

    if instance.option.type in MEMBERSHIP_OPTION_TYPE_IDS:

        membership_type = MembershipType.reverse(instance.suboption.name)

        membership, created = Membership.objects.get_or_create(
            attendee=instance.attendee,
            defaults={
                'user': instance.attendee.user,
                'bind_date': instance.attendee.event.startdate,
                'membership_type': membership_type
            })

        if not created and membership.membership_type != membership_type:
            membership.membership_type = membership_type
            membership.save()


@receiver(attendee_updated_signal)
def attendee_update_handler(sender, **kwargs):
    attendee = kwargs['attendee']

    state = Membership.objects.get_membership_state(attendee.user, attendee.event.startdate,
                                                    fake_upgrade_attendance_as_full=attendee)

    if state == MembershipState.ACTIVE:
        AttendeeComment.objects.filter(attendee=attendee, author='system.kitamembership').delete()
    else:
        AttendeeComment.objects.get_or_create(
            attendee=attendee,
            author='system.kitamembership',
            defaults={
                'check_in_announce': True,
                'comment': 'Denne bruger har ikke betalt kontingent.'
            }
        )

### Membership choice widget


class MembershipChoiceWidget(ChoiceWidget):

    def _get_choices(self, user, event):
        return Membership.objects.get_membership_choices(user, event)

    def update_choices(self, user, attendee):

        membership_choices = self._get_choices(user, self.option.group.event)
        price_label_pairs = [(Membership.objects.get_membership_price(choice), MembershipType.get_display_name(choice))
                             for choice in membership_choices]

        self.choices = self._get_or_create_choices(price_label_pairs,
                                                   default_label="Du er allerede medlem" if len(price_label_pairs) == 0 else "---")


class MembershipChoiceNoPassWidget(MembershipChoiceWidget):

    def _get_choices(self, user, event):
        return Membership.objects.get_membership_choices(user, event, allow_pass=False)


class MembershipTypeManager(ChoiceTypeManager):

    @staticmethod
    def get_widget(scope, option):
        if scope == SCOPE.SADMIN:
            return MembershipChoiceWidget(scope, option)
        else:
            return MembershipChoiceWidget(scope, option, send_notifications=True)


class MembershipWithoutPassTypeManager(ChoiceTypeManager):

    @staticmethod
    def get_widget(scope, option):
        if scope == SCOPE.SADMIN:
            return MembershipChoiceNoPassWidget(scope, option)
        else:
            return MembershipChoiceNoPassWidget(scope, option, send_notifications=True)


options.register_custom_type(MEMBERSHIP_OPTION_TYPE_ID, 'Kontingent', MembershipTypeManager)
options.register_custom_type(MEMBERSHIP_NOPASS_OPTION_TYPE_ID, 'Kontingent (ingen fripas)', MembershipWithoutPassTypeManager)

sadmin2.register_custom_stype(MEMBERSHIP_OPTION_TYPE_ID,
                              SBaseTypeManager(MEMBERSHIP_OPTION_TYPE_ID,
                                               create_form=option_form_factory(
                                                   Option,
                                                   ('name', 'description', 'required', 'depends_on', 'notify_on_selection'),
                                                   ('name', 'type', 'description', 'required', 'depends_on', 'notify_on_selection'),
                                                   MEMBERSHIP_OPTION_TYPE_ID),
                                               update_form=option_form_factory(
                                                    Option,
                                                    ('name', 'description', 'required', 'depends_on', 'notify_on_selection'),
                                                    ('name', 'type', 'description', 'required', 'depends_on', 'notify_on_selection'),
                                                    MEMBERSHIP_OPTION_TYPE_ID)))

sadmin2.register_custom_stype(MEMBERSHIP_NOPASS_OPTION_TYPE_ID,
                              SBaseTypeManager(MEMBERSHIP_NOPASS_OPTION_TYPE_ID,
                                               create_form=option_form_factory(
                                                   Option,
                                                   ('name', 'description', 'required', 'depends_on', 'notify_on_selection'),
                                                   ('name', 'type', 'description', 'required', 'depends_on', 'notify_on_selection'),
                                                   MEMBERSHIP_NOPASS_OPTION_TYPE_ID),
                                               update_form=option_form_factory(
                                                    Option,
                                                    ('name', 'description', 'required', 'depends_on', 'notify_on_selection'),
                                                    ('name', 'type', 'description', 'required', 'depends_on', 'notify_on_selection'),
                                                    MEMBERSHIP_NOPASS_OPTION_TYPE_ID)))


### Sadmin2 membership overview

menu.sadmin2_menu_tab_user.append({
    'id': 'membership',
    'name': _('Membership'),
    'url_callback': menu.url_callback('kita_membership_sadmin2', ('user_pk', ))
})

menu.sadmin2_menu_tab_users[1]['dropdown'] = list(menu.sadmin2_menu_tab_users[1]['dropdown'])
menu.sadmin2_menu_tab_users[1]['dropdown'].append({
    'id': 'membership',
    'name': _('Membership'),
    'url_callback': menu.url_callback('kita_membership_report_sadmin2', [])
})

menu.breadcrumbs['user_membership'] = {
    'name': _('Membership'),
    'url_callback': menu.url_callback('kita_membership_sadmin2', ('user_pk',)),
    'parent': 'user'
}

menu.breadcrumbs['user_membershipreport'] = {
    'name': _('Membership'),
    'url_callback': menu.url_callback('kita_membership_report_sadmin2', []),
    'parent': 'users_reports'
}