from django.template.loader import render_to_string
from django.contrib.admin.helpers import AdminForm

from selvbetjening.core.members.processor_handlers import user_migration_processors
from selvbetjening.core.events.processor_handlers import change_selection_processors, checkin_processors
from selvbetjening.portal.eventregistration.processor_handlers import signup_processors, change_processors

from forms import MembershipForm
import models

class UserMigrationProcessor(object):
    template_name = 'kitamembership/processors/user_migration.html'

    def __init__(self, request, old_user, new_user):
        self.request = request
        self.old_user = old_user
        self.new_user = new_user

        self.memberships = models.Membership.objects.filter(user=self.old_user)

    def is_valid(self):
        return True

    def render_function(self):
        return render_to_string(self.template_name,
                                {'count': self.memberships.count()})


    def migrate(self):
        for membership in self.memberships:
            membership.user = self.new_user
            membership.save()

user_migration_processors.register(UserMigrationProcessor)

class ChangeSelectionProcessor(object):
    def __init__(self, request, attendee):
        self.request = request
        self.attendee = attendee

        self.membership_choices = models.Membership.objects.get_membership_choices(user=attendee.user,
                                                                                   event=attendee.event,
                                                                                   invoice=attendee.invoice)

        self.previous_state = models.Membership.objects.get_membership_state(attendee.user,
                                                                             attendee.event,
                                                                             handle_as_unpaid_invoice=[attendee.invoice])
        try:
            self.existing_membership = models.Membership.objects.get(user=attendee.user,
                                                                     event=attendee.event,
                                                                     invoice=attendee.invoice)
        except models.Membership.DoesNotExist:
            self.existing_membership = None

        if len(self.membership_choices) == 0 and self.existing_membership:
            self.membership_choices = [models.MembershipType.NONE,
                                       self.existing_membership.membership_type]

        self.submit_allowed = False

        if len(self.membership_choices) == 0:
            self.submit_allowed = True
        elif request.method == 'POST':
            self.form = MembershipForm(request.POST,
                                       attendee=attendee,
                                       membership_choices=self.membership_choices)
            if self.form.is_valid():
                self.submit_allowed = True
        else:
            self.form = MembershipForm(attendee=attendee,
                                       membership_choices=self.membership_choices)

    def view(self):
        if len(self.membership_choices) == 0:
            return render_to_string('kitamembership/checkin/ismember.html',
                                    {'attendee' : self.attendee,
                                     'previous_state' : self.previous_state,
                                     'existing_membership': self.existing_membership})
        else:
            return render_to_string('kitamembership/checkin/form.html',
                                    {'form' : self.form,
                                     'attendee' : self.attendee,
                                     'previous_state': self.previous_state,
                                     })

    def is_valid(self):
        return self.submit_allowed

    def save(self):
        if not len(self.membership_choices) == 0:
            self.form.save()

change_selection_processors.register(ChangeSelectionProcessor)

class CheckinProcessor(object):
    def __init__(self, request, attendee):
        self.request = request
        self.attendee = attendee

        self.state = models.Membership.objects.get_membership_state(attendee.user,
                                                                    attendee.event,
                                                                    handle_as_paid_invoice=[attendee.invoice])

        self.previous_state = models.Membership.objects.get_membership_state(attendee.user,
                                                                             attendee.event,
                                                                             handle_as_unpaid_invoice=[attendee.invoice])

    def view(self):
        if self.state is not models.MembershipState.ACTIVE:
            return render_to_string('kitamembership/checkin/notmemberwarning.html',
                                    {'attendee' : self.attendee,
                                     'previous_state' : self.previous_state})

        else:
            return render_to_string('kitamembership/checkin/ismember.html',
                                    {'attendee' : self.attendee,
                                     'previous_state' : self.previous_state})

checkin_processors.register(CheckinProcessor)

class SignupOrChangeProcessor(object):
    def __init__(self, request, **kwargs):
        self.request = request

        self.post_allowed = False

        if request.method == 'POST':
            self.form = MembershipForm(request.POST, **kwargs)
            self.post_allowed = self.form.is_valid()
        else:
            self.form = MembershipForm(**kwargs)

    def is_valid(self):
        if self.form.has_options():
            return self.post_allowed
        else:
            return True

    def view(self):
        if self.form.has_options():
            return render_to_string('kitamembership/signup/signup.html',
                                    {'form' : self.form})
        else:
            return ''

    def save(self, attendee=None):
        if self.form.has_options():
            if attendee is not None:
                self.form.save(attendee.invoice)
            else:
                self.form.save()


class SignupProcessor(SignupOrChangeProcessor):
    def __init__(self, request, user, event):
        super(SignupProcessor, self).__init__(request, user=user, event=event)

signup_processors.register(SignupProcessor)

class ChangeProcessor(SignupOrChangeProcessor):
    def __init__(self, request, attendee, optionforms):
        super(ChangeProcessor, self).__init__(request, attendee=attendee)
        
    def postsave(self):
        pass

change_processors.register(ChangeProcessor)
