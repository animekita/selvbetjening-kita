from datetime import datetime, timedelta

from django.test import TestCase
from django.contrib.auth import models as auth_models
from selvbetjening.core.events.models import OptionGroup, Attend
from selvbetjening.core.events.options.dynamic_selections import dynamic_selections_form_factory, dynamic_selections, \
    _pack_id
from selvbetjening.core.events.options.scope import SCOPE

from selvbetjening.core.events.tests import Database as EventDatabase

from models import MembershipType, MembershipState, Membership
from selvbetjening.core.user.models import SUser


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
        return SUser.objects.create_user(id, '%s@example.org' % id, id)


class MembershipModelTestCase(TestCase):
    def setUp(self):

        self.date_inactive = datetime(datetime.now().year - 2, datetime.now().month, datetime.now().day)
        self.date_passive = datetime(datetime.now().year - 1, datetime.now().month, datetime.now().day)
        self.date_active = datetime.now() - timedelta(days=5)

    def test_no_payments(self):
        user = Database.new_user()

        self.assertEqual(MembershipState.INACTIVE,
                         Membership.objects.get_membership_state(user, datetime.today()))

    def test_full_payment_inactive(self):
        user = Database.new_user()

        self.assertEqual(MembershipState.INACTIVE,
                         Membership.objects.get_membership_state(user, datetime.today()))

    def test_full_payment_passive(self):
        user = Database.new_user()
        event = EventDatabase.new_event(start_date=self.date_passive)
        attendee = EventDatabase.attend(user, event)

        Membership.objects.create(user=user,
                                  attendee=attendee,
                                  bind_date=self.date_passive,
                                  membership_type=MembershipType.FULL)

        self.assertEqual(MembershipState.PASSIVE,
                         Membership.objects.get_membership_state(user, datetime.today()))

    def test_full_payment_active(self):
        user = Database.new_user()
        event = EventDatabase.new_event(start_date=self.date_active)
        attendee = EventDatabase.attend(user, event)

        Membership.objects.create(user=user,
                                  attendee=attendee,
                                  bind_date=self.date_active,
                                  membership_type=MembershipType.FULL)

        self.assertEqual(MembershipState.ACTIVE,
                         Membership.objects.get_membership_state(user, datetime.today()))

        self.assertNotEqual(Membership.objects.member_since(user), None)

    def test_frate_payment_inactive(self):
        user = Database.new_user()
        event = EventDatabase.new_event(start_date=self.date_inactive)
        attendee = EventDatabase.attend(user, event)

        Membership.objects.create(user=user,
                                  attendee=attendee,
                                  bind_date=self.date_inactive,
                                  membership_type=MembershipType.FRATE)

        self.assertEqual(MembershipState.INACTIVE,
                         Membership.objects.get_membership_state(user, datetime.today()))

    def test_frate_payment_passive(self):
        user = Database.new_user()
        event = EventDatabase.new_event(start_date=self.date_passive)
        attendee = EventDatabase.attend(user, event)

        Membership.objects.create(user=user,
                                  attendee=attendee,
                                  bind_date=self.date_passive,
                                  membership_type=MembershipType.FRATE)

        self.assertEqual(MembershipState.PASSIVE,
                         Membership.objects.get_membership_state(user, datetime.today()))

    def test_frate_payment_condactive(self):
        user = Database.new_user()
        event = EventDatabase.new_event(start_date=self.date_active)
        attendee = EventDatabase.attend(user, event)

        Membership.objects.create(user=user,
                                  attendee=attendee,
                                  bind_date=self.date_active,
                                  membership_type=MembershipType.FRATE)

        self.assertEqual(MembershipState.CONDITIONAL_ACTIVE,
                         Membership.objects.get_membership_state(user, datetime.today()))

    def test_srate_payment_inactive(self):
        user = Database.new_user()
        event = EventDatabase.new_event(start_date=self.date_inactive)
        attendee = EventDatabase.attend(user, event)

        Membership.objects.create(user=user,
                                  attendee=attendee,
                                  bind_date=self.date_inactive,
                                  membership_type=MembershipType.FRATE)

        event = EventDatabase.new_event(start_date=self.date_inactive + timedelta(days=1))
        attendee = EventDatabase.attend(user, event)

        Membership.objects.create(user=user,
                                  attendee=attendee,
                                  bind_date=self.date_inactive + timedelta(days=1),
                                  membership_type=MembershipType.SRATE)

        self.assertEqual(MembershipState.INACTIVE,
                         Membership.objects.get_membership_state(user, datetime.today()))

    def test_srate_payment_passive(self):
        user = Database.new_user()
        event = EventDatabase.new_event(start_date=self.date_passive)
        attendee = EventDatabase.attend(user, event)

        Membership.objects.create(user=user,
                                  attendee=attendee,
                                  bind_date=self.date_passive,
                                  membership_type=MembershipType.FRATE)

        event = EventDatabase.new_event(start_date=self.date_passive + timedelta(days=1))
        attendee = EventDatabase.attend(user, event)

        Membership.objects.create(user=user,
                                  attendee=attendee,
                                  bind_date=self.date_passive + timedelta(days=1),
                                  membership_type=MembershipType.SRATE)

        self.assertEqual(MembershipState.PASSIVE,
                         Membership.objects.get_membership_state(user, datetime.today()))

    def test_srate_payment_active(self):
        user = Database.new_user()
        event = EventDatabase.new_event(start_date=self.date_active)
        attendee = EventDatabase.attend(user, event)

        Membership.objects.create(user=user,
                                  attendee=attendee,
                                  bind_date=self.date_active,
                                  membership_type=MembershipType.FRATE)

        event = EventDatabase.new_event(start_date=self.date_active + timedelta(days=1))
        attendee = EventDatabase.attend(user, event)

        Membership.objects.create(user=user,
                                  attendee=attendee,
                                  bind_date=self.date_active + timedelta(days=1),
                                  membership_type=MembershipType.SRATE)

        self.assertEqual(MembershipState.ACTIVE,
                         Membership.objects.get_membership_state(user, datetime.today()))


class MembershipWidgetTestCase(TestCase):
    fixtures = ['kita_test_fixtures.json']

    def test_membership_widget_new_user_not_selecting_anything(self):

        option_group = OptionGroup.objects.get(pk=1)
        attendee = Attend.objects.get(pk=1)

        OptionGroupSelectionsForm = dynamic_selections_form_factory(SCOPE.EDIT_REGISTRATION, option_group)
        form = OptionGroupSelectionsForm({}, user=attendee.user, attendee=attendee)

        self.assertTrue(form.is_valid())  # not required, so this is okay
        self.assertTrue(hasattr(form, 'cleaned_data'))

        form.save()

        self.assertEqual(Membership.objects.all().count(), 1)

    def test_membership_widget_new_user(self):

        option_group = OptionGroup.objects.get(pk=1)
        attendee = Attend.objects.get(pk=1)

        OptionGroupSelectionsForm = dynamic_selections_form_factory(SCOPE.EDIT_REGISTRATION, option_group)
        form = OptionGroupSelectionsForm({
            _pack_id('option', 1): _pack_id('suboption', 1)
        }, user=attendee.user, attendee=attendee)

        self.assertTrue(form.is_valid())  # not required, so this is okay
        self.assertTrue(hasattr(form, 'cleaned_data'))

        form.save()

        self.assertEqual(Membership.objects.all().count(), 2)

    def test_membership_widget_required_new_user_not_selecting_anything(self):

        option_group = OptionGroup.objects.get(pk=2)
        attendee = Attend.objects.get(pk=1)

        OptionGroupSelectionsForm = dynamic_selections_form_factory(SCOPE.EDIT_REGISTRATION, option_group)
        form = OptionGroupSelectionsForm({}, user=attendee.user, attendee=attendee)

        self.assertFalse(form.is_valid())

    def test_membership_widget_required_new_user(self):

        option_group = OptionGroup.objects.get(pk=2)
        attendee = Attend.objects.get(pk=1)

        OptionGroupSelectionsForm = dynamic_selections_form_factory(SCOPE.EDIT_REGISTRATION, option_group)
        form = OptionGroupSelectionsForm({
            _pack_id('option', 2): _pack_id('suboption', 5)
        }, user=attendee.user, attendee=attendee)

        self.assertTrue(form.is_valid())
        self.assertTrue(hasattr(form, 'cleaned_data'))

        form.save()

        self.assertEqual(Membership.objects.all().count(), 2)

    def test_membership_widget_required_new_user_trying_to_cheat(self):

        option_group = OptionGroup.objects.get(pk=2)
        attendee = Attend.objects.get(pk=1)

        OptionGroupSelectionsForm = dynamic_selections_form_factory(SCOPE.EDIT_REGISTRATION, option_group)
        form = OptionGroupSelectionsForm({
            _pack_id('option', 2): '__EMPTY__'
        }, user=attendee.user, attendee=attendee)

        self.assertFalse(form.is_valid())

    ### Has a membership, so now the from should show no options

    def test_membership_widget_member_not_selecting_anything(self):

        option_group = OptionGroup.objects.get(pk=1)
        attendee = Attend.objects.get(pk=2)

        OptionGroupSelectionsForm = dynamic_selections_form_factory(SCOPE.EDIT_REGISTRATION, option_group)
        form = OptionGroupSelectionsForm({}, user=attendee.user, attendee=attendee)

        self.assertTrue(form.is_valid())  # not required, so this is okay
        self.assertTrue(hasattr(form, 'cleaned_data'))

        form.save()

        self.assertEqual(Membership.objects.all().count(), 1)

    def test_membership_widget_required_member_not_selecting_anything(self):

        option_group = OptionGroup.objects.get(pk=2)
        attendee = Attend.objects.get(pk=2)

        OptionGroupSelectionsForm = dynamic_selections_form_factory(SCOPE.EDIT_REGISTRATION, option_group)
        form = OptionGroupSelectionsForm({
            _pack_id('option', 2): '__EMPTY__'
        }, user=attendee.user, attendee=attendee)

        self.assertTrue(form.is_valid())


