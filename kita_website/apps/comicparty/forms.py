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

    accept = forms.BooleanField(required=True, label='Jeg accepterer nedenstående vilkår',
                                help_text='De oplysninger der er blevet opgivet i denne formular vil blive sendt til tredjepart (Alpha Entertainment) for videre behandling. Anime Kita formidler blot kontakten mellem dig og Alpha Entertainment og er derfor ikke ansvarlig for det videre salgsforløb.')

    helper = FormHelper()
    helper.add_layout(Layout(InlineFieldset('Comic Party bestillingsformular',
                                            'subscription',),
                             InlineFieldset('Modtager adresse',
                                            'name', 'street', 'postalcode', 'city',),
                             InlineFieldset('Kontakt',
                                            'email', 'comment'),
                             InlineFieldset('',
                                            'accept'),
                      ))

    helper.add_input(Submit('order', 'Send bestilling'))
    helper._form_action = '#formular'

