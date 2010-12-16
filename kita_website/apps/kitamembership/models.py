from datetime import datetime, timedelta

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from selvbetjening.core.invoice.models import Invoice
from selvbetjening.core.invoice.signals import populate_invoice
from selvbetjening.core.events.models import Event, Attend

from django.db.models.signals import post_delete, post_save

import processors # important, used to register processors

class MembershipState(object):
    INACTIVE = 'INACTIVE'
    PASSIVE = 'PASSIVE'
    CONDITIONAL_ACTIVE = 'CONDITIONAL_ACTIVE'
    ACTIVE = 'ACTIVE'

    @staticmethod
    def get_display_name(membership_state):
        names = {'INACTIVE' : _('Inactive member'),
                 'PASSIVE' : _('Passive member'),
                 'CONDITIONAL_ACTIVE' : _('Conditional active member'),
                 'ACTIVE' : _('Active member')}

        return unicode(names.get(membership_state, membership_state))

    @staticmethod
    def get_display_name_short(membership_state):
        names = {'INACTIVE' : _('Inactive'),
                 'PASSIVE' : _('Passive'),
                 'CONDITIONAL_ACTIVE' : _('Conditional active'),
                 'ACTIVE' : _('Active')}

        return unicode(names.get(membership_state, membership_state))

class MembershipType(object):
    FULL = 'FULL'
    FRATE = 'FRATE'
    SRATE = 'SRATE'

    NONE = 'NONE'

    @staticmethod
    def get_display_name(membership_type):
        names = {'FULL' : _('Full payment'),
                 'FRATE' : _('First rate'),
                 'SRATE' : _('Second rate'),
                 'NONE' : _('No membership payment')}

        return unicode(names.get(membership_type, membership_type))

class MembershipManager(models.Manager):
    def create(self, **kwargs):
        invoice = kwargs.get('invoice', None)

        if invoice is None:
            invoice = Invoice.objects.create(user=kwargs['user'],
                                             name='Payment')
            kwargs['invoice'] = invoice

        return super(MembershipManager, self).create(**kwargs)

    def get_membership_state(self, user, event=None, handle_as_paid_invoice=None, handle_as_unpaid_invoice=None):
        if handle_as_paid_invoice is None:
            handle_as_paid_invoice = []

        if handle_as_unpaid_invoice is None:
            handle_as_unpaid_invoice = []

        memberships = []
        for membership in Membership.objects.filter(user=user).order_by('-bind_date'):
            if membership.invoice not in handle_as_unpaid_invoice and \
               (membership.invoice.is_paid() or membership.invoice in handle_as_paid_invoice):
                memberships.append(membership)

        if len(memberships) == 0:
            return MembershipState.INACTIVE

        if memberships[0].membership_type == 'SRATE':
            last = memberships[1]
        else:
            last = memberships[0]

        payment_quater = self.total_quaters(last.bind_date)
        date_in_quaters = self.total_quaters(datetime.now())

        if payment_quater + 8 <= date_in_quaters:
            return MembershipState.INACTIVE
        elif payment_quater + 4 <= date_in_quaters:
            return MembershipState.PASSIVE
        else:
            if memberships[0].membership_type == 'FULL' or memberships[0].membership_type == 'SRATE':
                return MembershipState.ACTIVE
            else:
                if event is not None and memberships[0].event == event:
                    return MembershipState.ACTIVE
                else:
                    return MembershipState.CONDITIONAL_ACTIVE

    def is_member(self, user, event=None):
        return self.get_membership_state(user, event) == MembershipState.ACTIVE

    def get_membership_choices(self, user, event=None, invoice=None):
        if invoice is None:
            invoice = []
        else:
            invoice = [invoice]

        state = self.get_membership_state(user,
                                          event,
                                          handle_as_unpaid_invoice=invoice)

        if state == MembershipState.ACTIVE:
            return []
        elif state == MembershipState.CONDITIONAL_ACTIVE:
            return [MembershipType.SRATE]
        else:
            return [MembershipType.FULL,
                    MembershipType.FRATE]

    def select_membership(self, user, membership_type, date=None, event=None, invoice=None):
        assert not (date is not None and event is not None)

        if event is not None:
            date = event.startdate

        if date is None:
            date = datetime.now()

        if invoice is not None:
            try:
                membership = Membership.objects.get(invoice=invoice)

                membership.membership_type = membership_type
                membership.save()

                return invoice
            except Membership.DoesNotExist:
                pass

        membership = self.create(user=user,
                                 invoice=invoice,
                                 event=event,
                                 membership_type=membership_type,
                                 bind_date=date)

        return membership.invoice

    def get_membership(self, user, invoice):
        try:
            membership = self.get(user=user, invoice=invoice)
            return membership.membership_type
        except:
            return None

    def last_member_period(self, user):
        """ Returns the timestamp marking the beginning of the last user membership period """
        memberships = Membership.objects.filter(user=user).order_by('-bind_date')

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
    """
    user = models.ForeignKey(User, verbose_name=_(u'user'))
    invoice = models.ForeignKey(Invoice, blank=True)

    event = models.ForeignKey(Event, blank=True, null=True)

    bind_date = models.DateTimeField()
    membership_type = models.CharField(max_length=5)

    objects = MembershipManager()

    class Meta:
        unique_together = (('user', 'invoice'),)

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

def update_invoice_handler(sender, **kwargs):
    instance = kwargs['instance']
    instance.invoice.update()

post_delete.connect(update_invoice_handler, sender=Membership)
post_save.connect(update_invoice_handler, sender=Membership)

def delete_membership_on_event_signoff(sender, **kwargs):
    instance = kwargs['instance']

    try:
        membership = Membership.objects.get(invoice=instance.invoice)
        membership.delete()

    except Membership.DoesNotExist:
        pass

post_delete.connect(delete_membership_on_event_signoff, sender=Attend)

def update_invoice_with_membership_handler(sender, **kwargs):
    invoice_revision = kwargs['invoice_revision']
    invoice = invoice_revision.invoice

    for membership in Membership.objects.filter(invoice=invoice):
        invoice_revision.add_line(description=unicode(membership),
                                  price=membership.price,
                                  managed=True)

populate_invoice.connect(update_invoice_with_membership_handler)

class YearlyRate(models.Model):
    year = models.IntegerField(max_length=4)
    rate = models.DecimalField(max_digits=6, decimal_places=2)

    def __unicode__(self):
        return _(u"Yearly rate for %s") % self.year