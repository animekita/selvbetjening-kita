# encoding: utf-8

from django import forms
from django.utils.translation import ugettext as _

from crispy_forms.layout import Layout
from crispy_forms.helper import FormHelper

from selvbetjening.viewbase.forms.helpers import SFieldset

import models

class MembershipForm(forms.Form):
    type = forms.ChoiceField(label=_('Payment type'))

    layout = Layout(SFieldset(u'Medlemskab', 'type',
                                   help_text=u'For at deltage i dette arrangement skal du betale kontingent. <a href="http://www.anime-kita.dk/bliv-medlem/">Du kan læse mere om vores kontingent og forskellen på fuldt kontingent og første/anden rate betalinger her</a>.'))

    helper = FormHelper()
    helper.add_layout(layout)
    helper.form_tag = False

    def __init__(self, *args, **kwargs):
        self.attendee = kwargs.pop('attendee', None)

        if self.attendee is None:
            self.user = kwargs.pop('user')
            self.event = kwargs.pop('event', None)
            self.invoice = None
        else:
            self.user = self.attendee.user
            self.event = self.attendee.event
            self.invoice = self.attendee.invoice

        membership_choices = kwargs.pop('membership_choices', None)

        if membership_choices is None:
            membership_choices = models.Membership.objects.get_membership_choices(self.user,
                                                                                  self.event,
                                                                                  self.invoice)

        if models.MembershipType.SRATE in membership_choices:
            description = _('Second rate payment description')
        else:
            description = _('First or full rate payment description')

        class Meta:
            layout = (
                (_('Choose membership payment'), ('type',), description),
                )

        self.Meta = Meta

        if self.attendee is not None:
            kwargs['initial'] = {'type' : models.Membership.objects.get_membership(self.user, self.attendee.invoice)}

        super(MembershipForm, self).__init__(*args, **kwargs)

        self.choices = [(membership_choice,
                         models.MembershipType.get_display_name(membership_choice))
                        for membership_choice in membership_choices]

        self.fields['type'].choices = self.choices

    def clean_type(self):
        if self.cleaned_data['type'] in [choice[0] for choice in self.choices]:
            return self.cleaned_data['type']

        raise forms.ValidationError(_("Payment type not valid"))

    def has_options(self):
        return len(self.choices) > 0

    def is_valid(self):
        if self.has_options():
            return super(MembershipForm, self).is_valid()

        return True

    def save(self, invoice=None):
        if self.attendee is not None:
            invoice = self.attendee.invoice

        if self.cleaned_data['type'] == models.MembershipType.NONE:
            if invoice is not None:
                models.Membership.objects.filter(event=self.event)\
                      .filter(invoice=invoice)\
                      .delete()

        elif self.has_options():
            models.Membership.objects.select_membership(self.user, self.cleaned_data['type'], event=self.event, invoice=invoice)
