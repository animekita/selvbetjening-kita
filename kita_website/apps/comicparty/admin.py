from django.utils.translation import ugettext as _
from django.db.models import Count
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.admin.helpers import AdminForm

from selvbetjening.core.events.models import Event, AttendState, Attend,\
     payment_registered_source
from selvbetjening.core.invoice.models import Invoice, Payment
from selvbetjening.core.mailcenter.sources import Source

from selvbetjening.sadmin.base import admin_formize
from selvbetjening.sadmin.base.sadmin import SAdminContext, SModelAdmin

from models import Order

class OrderAdmin(SModelAdmin):
    class Meta:
        app_name = 'comicparty'
        name = 'order'
        model = Order

    list_display = ('user', 'timestamp')
    search_fields = ('user',)

    #def add_view(self, request, extra_context=None):
        #extra_context = extra_context or {}
        #extra_context['menu'] = nav.events_menu.render()
        #return super(EventAdmin, self).add_view(request, extra_context=extra_context)

    #def change_view(self, request, object_id, extra_context=None):
        #extra_context = extra_context or {}
        #extra_context['menu'] = nav.event_menu.render(event_pk=object_id)
        #return super(EventAdmin, self).change_view(request, object_id, extra_context)

    #def changelist_view(self, request, extra_context=None):
        #extra_context = extra_context or {}
        #extra_context['menu'] = nav.events_menu.render()
        #extra_context['title'] = _(u'Browse Events')
        #return super(EventAdmin, self).changelist_view(request, extra_context)
