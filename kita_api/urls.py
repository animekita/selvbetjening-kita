from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^', include('selvbetjening.api.sso.urls')),
)
