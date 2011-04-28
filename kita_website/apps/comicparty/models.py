# -- encoding: utf8 --

from datetime import timedelta

from django.db import models
from django.utils.translation import ugettext as _

from django.contrib.auth.models import User

from selvbetjening.core.mailcenter.sources import Source

class Order(models.Model):
    SUBSCRIPTION_12 = 12
    SUBSCRIPTION_6 = 6

    SUBSCRIPTION_CHOICES = ((SUBSCRIPTION_6, '6 måneders abonnement'),
                            (SUBSCRIPTION_12, '12 måneders abonnement'))

    user = models.ForeignKey(User)

    subscription = models.IntegerField(choices=SUBSCRIPTION_CHOICES,
                                       default=SUBSCRIPTION_6,
                                       verbose_name='Abonnement')


    name = models.CharField(max_length=256, verbose_name='Navn')
    street = models.CharField(max_length=256, verbose_name='Vej')
    postalcode = models.IntegerField(verbose_name='Postnummer')
    city = models.CharField(max_length=256, verbose_name='By')

    email = models.EmailField(verbose_name='E-mail',
                              help_text='Du vil modtage instrukserne for betaling på denne e-mail.')

    comment = models.TextField(verbose_name='Kommentar', blank=True,
                               help_text='Kommentar til Alpha Entertainment.')

    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def already_ordered(self):
        return Order.objects.filter(user=self.user)\
                            .filter(timestamp__gt=self.timestamp - timedelta(days=4*30))\
                            .exclude(pk=self.pk)\
                            .exists()

# email sources

comicparty_order_source = Source('comicparty_order_signal',
                                 _(u'User orders Comic Party'),
                                 [Order])

from selvbetjening.sadmin.base.sadmin import site
from admin import OrderAdmin

site.register('comicparty', OrderAdmin)