from django.contrib import admin
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from selvbetjening.sadmin.base.sadmin import SBoundModelAdmin, site

from models import Membership, YearlyRate, MembershipState

class MembershipAdmin(SBoundModelAdmin):
    class Meta:
        app_name = 'kitamembership'
        name = 'membership'
        model = Membership
        bound_model = User

        display_name = _(u'Kita Membership')
        display_name_plural = _(u'Kita Memberships')

    def paid(membership):
        return membership.invoice.is_paid()
    paid.boolean = True

    list_display = ('membership_type', 'bind_date', 'event', paid)

    fieldsets = (
        (None, {
            'fields' : ('bind_date', 'membership_type', 'event'),
        }),
    )

    def __init__(self):
        super(MembershipAdmin, self).__init__()

    def queryset(self, request):
        qs = super(MembershipAdmin, self).queryset(request)

        return qs.filter(user=request.bound_object)

    def _init_navigation(self):
        super(MembershipAdmin, self)._init_navigation()

        # insert reference of this admin into members admin
        from django.conf.urls.defaults import patterns, url, include

        from selvbetjening.sadmin.members import models # ensure members admin is instanisated
        user_admin = site.get('members')
        old_get_urls = user_admin.get_urls
        local_urls = self.urls

        def overwrite_get_urls():
            urlpatterns = patterns('',
                                   ('^(?P<bind_pk>[0-9]+)/membership/', include(local_urls))
            ) + old_get_urls()

            return urlpatterns

        user_admin.get_urls = overwrite_get_urls

        # insert references into members admin
        self.module_menu = user_admin.object_menu
        self.page_root.parent = user_admin.page_change
        user_admin.object_menu.register(self.page_root, title=_('Membership'))

    def save_form(self, request, form, change):
        instance = form.save(commit=False)

        if not change:
            instance.user = request.bound_object

        return instance

    #def get_urls(self):

        ##

        ##info = self.model._meta.app_label, self.model._meta.module_name

        ##urlpatterns = patterns('',
                               ###url(r'^statistics/',
                                   ###self.admin_site.admin_view(admin_views.membership_statistics),
                                   ###{'model_admin': self},
                                   ###name='%s_%s_statistics' % info),
                               ###)

        ##urlpatterns +=

        #return super(MembershipAdmin, self).get_urls()

        #return urlpatterns

    #def membership_statistics(request,
                              #model_admin,
                              #template_name='admin/kitamembership/membership/statistics.html'):

        #if not model_admin.has_change_permission(request, None):
            #raise PermissionDenied

        #active = 0
        #conditional_active = 0
        #passive = 0
        #inactive = 0

        #for user in User.objects.all():
            #state = Membership.objects.get_membership_state(user)

            #if state == MembershipState.ACTIVE:
                #active += 1
            #elif state == MembershipState.CONDITIONAL_ACTIVE:
                #conditional_active += 1
            #elif state == MembershipState.PASSIVE:
                #passive += 1
            #else:
                #inactive += 1

        #return render_to_response(template_name,
                                  #{'active': active,
                                   #'conditional_active' : conditional_active,
                                   #'passive' : passive,
                                   #'inactive': inactive,
                                   #'total' : active + conditional_active + passive},
                                  #context_instance=RequestContext(request))

#class YearlyRateAdmin(admin.ModelAdmin):
    #list_display = ('year', 'rate')

#site.register(YearlyRate, YearlyRateAdmin)

#class MembershipInline(admin.TabularInline):
    #model = Membership
    #extra = 0z