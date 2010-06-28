from selvbetjening.settings_base import *

import os
DIRNAME = os.path.abspath(os.path.dirname(__file__))

# email
DEFAULT_FROM_EMAIL = 'noreply@anime-kita.dk'
SERVER_EMAIL = 'noreply@anime-kita.dk'

# various settings
ROOT_URLCONF = 'kita_website.urls'

ADMINS = (
    #('admin', 'admin@example.org'),
)

# template directories
TEMPLATE_DIRS = [
    os.path.join(DIRNAME, 'templates')
] + TEMPLATE_DIRS

# installed applications
INSTALLED_APPS.extend([
    'selvbetjening.viewhelpers.forms',
    'selvbetjening.viewhelpers.googleanalytics',
    'selvbetjening.viewhelpers.copyright',

    'selvbetjening.clients.quickregistration',
    'selvbetjening.clients.mailcenter',
    'selvbetjening.clients.profile',
    'selvbetjening.clients.eventregistration',

    'selvbetjening.notify',
    'selvbetjening.notify.concrete5',
    'selvbetjening.notify.proftpd',

    'kita_website.apps.kitamembership',
    'kita_website.apps.eventlogger',
    'kita_website.apps.achivements',
])

# other instance settings
AUDIT_FILE = '/tmp/selvaudit.log'

# import localsettings, a per deployment configuration file
try:
    from settings_local import *
except ImportError:
    pass
