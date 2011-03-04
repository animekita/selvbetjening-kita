from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from selvbetjening.sadmin.base import nav

# main menu
#main_menu = nav.Navigation(_('Other'))
#nav.registry['main'].register(main_menu)

#main_menu.register(nav.Option(_(u'Browse Comic Party Orders'), 'sadmin:comicparty_order_changelist',
    #lambda user: user.has_perm('comicparty.change_order'))
#)