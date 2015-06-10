
from selvbetjening.settings_base import *

# email

DEFAULT_FROM_EMAIL = 'noreply@anime-kita.dk'
SERVER_EMAIL = 'noreply@anime-kita.dk'

# various settings

ROOT_URLCONF = 'kita_website.urls'

# template directories

THIS_DIR = os.path.abspath(os.path.dirname(__file__))

TEMPLATE_DIRS = [
    os.path.join(THIS_DIR, 'templates')
] + TEMPLATE_DIRS

# installed applications

INSTALLED_APPS.extend([
    'captcha',
    'selvbetjening.frontend.base',
    'selvbetjening.frontend.auth',
    'selvbetjening.frontend.userportal',
    'selvbetjening.frontend.eventsingle',
    'selvbetjening.frontend.eventportal',
    'selvbetjening.frontend.utilities',

    'selvbetjening.api.rest',
    'selvbetjening.api.sso',

    'kita_website.apps.kitamembership',
    #'kita_website.apps.achievements',
    'kita_website.apps.vanillaforum'
])

# policy

POLICY['PORTAL.EVENTREGISTRATION.COMBINED_EVENT'] = True
POLICY['VALIDATION.USER_LOCATION.REQUIRED'] = True

TEST_INCLUDE.append('kita_website')
