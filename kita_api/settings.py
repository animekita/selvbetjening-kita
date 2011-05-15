from selvbetjening.settings_base import *

DIRNAME = os.path.abspath(os.path.dirname(__file__))

# email
DEFAULT_FROM_EMAIL = 'noreply@anime-kita.dk'
SERVER_EMAIL = 'noreply@anime-kita.dk'

# various settings
ROOT_URLCONF = 'kita_api.urls'

ADMINS = (
    #('admin', 'admin@example.org'),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
)

TEMPLATE_DIRS = [
    os.path.join(DIRNAME, 'templates')
] + TEMPLATE_DIRS

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',

    'selvbetjening.api.sso'
)

# import localsettings, a per deployment configuration file
try:
    from settings_local import *
except ImportError:
    pass

TEMPLATE_DEBUG = False
