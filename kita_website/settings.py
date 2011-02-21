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
    'selvbetjening.viewbase.forms',
    'selvbetjening.viewbase.googleanalytics',
    'selvbetjening.viewbase.copyright',

    'selvbetjening.portal.quickregistration',
    'selvbetjening.portal.profile',
    'selvbetjening.portal.eventregistration',

    'selvbetjening.notify',
    'selvbetjening.notify.concrete5',
    'selvbetjening.notify.proftpd',
    'selvbetjening.notify.htdigest',
#    'selvbetjening.notify.vanillaforum',

    'selvbetjening.sadmin.base',
    'selvbetjening.sadmin.members',
    'selvbetjening.sadmin.events',
    'selvbetjening.sadmin.mailcenter',

    'kita_website.apps.kitamembership',
    'kita_website.apps.achivements',
    'kita_website.apps.vanillaforum',
    'kita_website.apps.comicparty',
])

# import localsettings, a per deployment configuration file
try:
    from settings_local import *
except ImportError:
    pass
