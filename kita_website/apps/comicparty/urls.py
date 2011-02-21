from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('kita_website.apps.comicparty.views',
    url('^godkendt/$', direct_to_template,
        kwargs={'template' : 'comicparty/accepted.html'},
        name='comicparty_accepted'),
    url('^$', 'register'),
)