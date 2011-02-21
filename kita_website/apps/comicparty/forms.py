# -- encoding: utf8 --

from datetime import datetime

from django import forms
from django.utils.translation import ugettext as _

from uni_form.helpers import FormHelper, Submit, Fieldset, Layout, Row

from selvbetjening.viewbase.forms.helpers import InlineFieldset

from models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user',)

    issue = forms.ChoiceField(label='Ønskede numre')

    accept = forms.BooleanField(required=True, label='Jeg accepterer nedenstående vilkår',
                                help_text='De oplysninger der er blevet opgivet i denne formular vil blive sendt til tredjepart (Alpha Entertainment) for videre behandling. Anime Kita formidler blot kontakten mellem dig og Alpha Entertainment og er derfor ikke ansvarlig for det videre salgsforløb.')

    helper = FormHelper()
    helper.add_layout(Layout(InlineFieldset('Comic Party bestillingsformular',
                                            'subscription', 'issue'),
                             InlineFieldset('Modtager adresse',
                                            'name', 'street', 'postalcode', 'city',),
                             InlineFieldset('Kontakt',
                                            'email', 'comment'),
                             InlineFieldset('',
                                            'accept'),
                      ))

    helper.add_input(Submit('order', 'Send bestilling'))
    helper._form_action = '#formular'

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)

        """
        Calculate the current available issue

        The first issue #1 was released February 2011

        Allow the sale of the next available issue, thus
        increment the current available issue by one when
        the current issue is released for sale.

        Thus, February and March 2011 issue #2 can be
        ordered. While April and May issue #3 can be
        ordered.

        The Algorithm
        -------------

        Denote February 2011 as month 0. For each two months
        a new issue is released, incrementing the available
        issue. The base value (issue # at month 0) is 2.

        Thus current available issue =
          2 + floor(months_since_first_issue / 2)

        """

        first = datetime(2011, 2, 1)
        now = datetime.now()

        months = (now.month + now.year * 12) - (first.month + first.year * 12)

        def issue_choice(months):
            current_issue = 2 + months / 2

            # (current_issue - 2) * 2 ensures that we are working with an equal month
            # + 2 pushes us two months ahead, the next release month
            next_release = (current_issue - 2) * 2 + 2

            date = datetime(first.year + next_release / 12,
                            first.month + next_release % 12,
                            1)

            text = 'Nummer #%s (%s) og frem' % (str(current_issue),
                                                _(date.strftime('%B')))

            return (current_issue, text)

        choices = (issue_choice(months),
                   issue_choice(months+2))

        self.fields['issue'].choices = choices
