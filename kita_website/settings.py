
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
    'selvbetjening.frontend.base',
    'selvbetjening.frontend.auth',
    'selvbetjening.frontend.eventsingle',
    'selvbetjening.frontend.eventportal',
    'selvbetjening.frontend.utilities',

    #'selvbetjening.api.rest',
    'selvbetjening.api.sso',

    #'kita_website.apps.kitamembership',
    #'kita_website.apps.achievements',
    'kita_website.apps.vanillaforum'
])

<<<<<<< HEAD
# south config

SOUTH_TESTS_MIGRATE = False

# policy

POLICY['PORTAL.EVENTREGISTRATION.ENFORCE_ADDRESS_UPDATE'] = True
=======
#POLICY['PORTAL.EVENTREGISTRATION.ENFORCE_ADDRESS_UPDATE'] = True
>>>>>>> hotfix/7.9.0

# import localsettings, a per deployment configuration file

try:
    from settings_local import *
except ImportError:
    pass
