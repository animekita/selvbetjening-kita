from datetime import datetime, timedelta

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth import models as auth_models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from selvbetjening.data.invoice.tests import Database as InvoiceDatabase
from selvbetjening.data.events.tests import Database as EventDatabase

from models import MembershipType, MembershipState, Membership, YearlyRate

class Database(object):
    _id = 0
    @classmethod
    def new_id(cls):
        cls._id += 1
        return str(cls._id)

    @classmethod
    def new_user(cls, id=None):
        if id is None:
            id = cls.new_id()
        return User.objects.create_user(id, '%s@example.org' % id, id)
    
    @classmethod
    def new_yearly_rate(cls, year=None):
        if year is None:
            year = datetime.now().year
        
        YearlyRate.objects.create(year=year,
                                  rate=100)
        
class MembershipModelTestCase(TestCase):
    def setUp(self):
        Database.new_yearly_rate()
        Database.new_yearly_rate(year=datetime.now().year - 2)
        Database.new_yearly_rate(year=datetime.now().year - 1)
        
        self.date_inactive = datetime(datetime.now().year - 2, datetime.now().month, datetime.now().day)
        self.date_passive = datetime(datetime.now().year - 1, datetime.now().month, datetime.now().day)
        self.date_active = datetime.now()

    def test_no_payments(self):
        user = Database.new_user()
        
        self.assertEqual(MembershipState.INACTIVE,
                         Membership.objects.get_membership_state(user))

    def test_full_payment_inactive(self):
        user = Database.new_user()
        invoice = Membership.select_membership(user, MembershipType.FULL, date=self.date_inactive)
        InvoiceDatabase.pay_invoice(invoice)
        
        self.assertEqual(MembershipState.INACTIVE,
                         Membership.objects.get_membership_state(user))

    def test_full_payment_passive(self):
        user = Database.new_user()
        invoice = Membership.select_membership(user, MembershipType.FULL, date=self.date_passive)
        InvoiceDatabase.pay_invoice(invoice)
        
        self.assertEqual(MembershipState.PASSIVE,
                         Membership.objects.get_membership_state(user))

    def test_full_payment_active(self):
        user = Database.new_user()
        invoice = Membership.select_membership(user, MembershipType.FULL, date=self.date_active)
        InvoiceDatabase.pay_invoice(invoice)
        
        self.assertEqual(MembershipState.ACTIVE,
                         Membership.objects.get_membership_state(user))

        self.assertNotEqual(Membership.objects.member_since(user), None)

    def test_frate_payment_inactive(self):
        user = Database.new_user()
        invoice = Membership.select_membership(user, MembershipType.FRATE, date=self.date_inactive)
        InvoiceDatabase.pay_invoice(invoice)
        
        self.assertEqual(MembershipState.INACTIVE,
                         Membership.objects.get_membership_state(user))

    def test_frate_payment_passive(self):
        user = Database.new_user()
        invoice = Membership.select_membership(user, MembershipType.FRATE, date=self.date_passive)
        InvoiceDatabase.pay_invoice(invoice)
        
        self.assertEqual(MembershipState.PASSIVE,
                         Membership.objects.get_membership_state(user))

    def test_frate_payment_condactive(self):
        user = Database.new_user()
        invoice = Membership.select_membership(user, MembershipType.FRATE, date=self.date_active)
        InvoiceDatabase.pay_invoice(invoice)
        
        self.assertEqual(MembershipState.CONDITIONAL_ACTIVE,
                         Membership.objects.get_membership_state(user))

    def test_srate_payment_inactive(self):
        user = Database.new_user()
        
        invoice = Membership.select_membership(user, MembershipType.FRATE, date=self.date_inactive)
        InvoiceDatabase.pay_invoice(invoice)
        
        invoice = Membership.select_membership(user, MembershipType.SRATE, date=self.date_inactive + timedelta(minutes=1))
        InvoiceDatabase.pay_invoice(invoice)
        
        self.assertEqual(MembershipState.INACTIVE,
                         Membership.objects.get_membership_state(user))

    def test_srate_payment_passive(self):
        user = Database.new_user()
        
        invoice = Membership.select_membership(user, MembershipType.FRATE, date=self.date_passive)
        InvoiceDatabase.pay_invoice(invoice)
        
        invoice = Membership.select_membership(user, MembershipType.SRATE, date=self.date_passive + timedelta(minutes=1))
        InvoiceDatabase.pay_invoice(invoice)
  
        self.assertEqual(MembershipState.PASSIVE,
                         Membership.objects.get_membership_state(user))

    def test_srate_payment_active(self):
        user = Database.new_user()
        
        invoice = Membership.select_membership(user, MembershipType.FRATE, date=self.date_active)
        InvoiceDatabase.pay_invoice(invoice)
        
        invoice = Membership.select_membership(user, MembershipType.SRATE, date=self.date_active + timedelta(minutes=1))
        InvoiceDatabase.pay_invoice(invoice)

        self.assertEqual(MembershipState.ACTIVE,
                         Membership.objects.get_membership_state(user))

    def test_full_payment_passive_no_date(self):
        user = Database.new_user()
        invoice = Membership.select_membership(user, MembershipType.FULL, date=datetime(2008, 1, 12, 18, 19, 45))
        InvoiceDatabase.pay_invoice(invoice)
        
        self.assertEqual(MembershipState.PASSIVE,
                         Membership.objects.get_membership_state(user))

        self.assertNotEqual(Membership.objects.passive_to(user), None)

        
    def test_no_payments(self):
        user = Database.new_user()
        
        self.assertFalse(Membership.is_member(user))
        
    def test_full_payment(self):
        user = Database.new_user()
        invoice = Membership.select_membership(user, MembershipType.FULL)
        InvoiceDatabase.pay_invoice(invoice)
        
        self.assertTrue(invoice.is_paid())
        self.assertTrue(Membership.is_member(user))
        
    def test_full_payment_not_paid(self):
        user = Database.new_user()
        invoice = Membership.select_membership(user, MembershipType.FULL)
        
        self.assertFalse(invoice.is_paid())
        self.assertFalse(Membership.is_member(user))
        
    def test_first_rate_payment(self):
        user = Database.new_user()
        invoice = Membership.select_membership(user, MembershipType.FRATE)
        InvoiceDatabase.pay_invoice(invoice)
        
        self.assertFalse(Membership.is_member(user))

    def test_full_overwrite(self):
        user = Database.new_user()
        
        invoice = Membership.select_membership(user, 
                                        MembershipType.FRATE,
                                        date=datetime.now() - timedelta(days=1))
        InvoiceDatabase.pay_invoice(invoice)
        
        invoice = Membership.select_membership(user, MembershipType.FULL)
        InvoiceDatabase.pay_invoice(invoice)
        
        self.assertTrue(Membership.is_member(user))        
        
    def test_secondrate_payment(self):
        user = Database.new_user()
        
        invoice = Membership.select_membership(user, 
                                        MembershipType.FRATE,
                                        date=datetime.now() - timedelta(days=1))
        InvoiceDatabase.pay_invoice(invoice)
        
        invoice = Membership.select_membership(user, MembershipType.SRATE)
        InvoiceDatabase.pay_invoice(invoice)
        
        self.assertTrue(Membership.is_member(user))
        
    def test_first_rate_event(self):
        user = Database.new_user()
        event = EventDatabase.new_event()
        
        invoice = Membership.select_membership(user,
                                        MembershipType.FRATE,
                                        event=event)
        InvoiceDatabase.pay_invoice(invoice)
        
        self.assertFalse(Membership.is_member(user))
        self.assertTrue(Membership.is_member(user, event=event))
        
class MembershipFormTestCase(TestCase):

    def setUp(self):
        self.user1 = auth_models.User.objects.create_user('user1', 'user1', 'user@example.org')

    def test_valid_options(self):
        f = forms.MembershipForm({'type' : 'FULL'}, user=self.user1)

        self.assertTrue(f.is_valid())

    def test_invalid_option(self):
        f = forms.MembershipForm({'type' : 'DOH'}, user=self.user1)

        self.assertFalse(f.is_valid())

    def test_save(self):
        f = forms.MembershipForm({'type' : 'FULL'}, user=self.user1)
        self.assertTrue(f.is_valid())
        f.save()

        self.assertTrue(Membership.is_member(self.user1))
        
        
        