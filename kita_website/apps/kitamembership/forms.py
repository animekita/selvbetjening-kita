from django.conf import settings

from selvbetjening.businesslogic.members.forms import UserRegistrationForm
from selvbetjening.frontend.utilities.forms import S2Fieldset

from captcha.fields import ReCaptchaField


class CaptchaUserRegistrationForm(UserRegistrationForm):
    captcha = ReCaptchaField()

    def __init__(self, *args, **kwargs):
        super(CaptchaUserRegistrationForm, self).__init__(*args, **kwargs)
        self.helper.layout.fields.append(
            S2Fieldset(None, 'captcha', collapse=False))

        fields = list(self.Meta.fields)
        fields.append('captcha')
        self.Meta.fields = fields
