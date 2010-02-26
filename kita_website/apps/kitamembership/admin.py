from django.contrib import admin
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext_lazy as _

from selvbetjening.core.selvadmin.admin import site, reverse_lazy

from models import Membership, YearlyRate
import admin_views

class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'bind_date', 'membership_type')

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url

        info = self.model._meta.app_label, self.model._meta.module_name

        urlpatterns = patterns('',
                               url(r'^statistics/',
                                   self.admin_site.admin_view(admin_views.membership_statistics),
                                   {'model_admin': self},
                                   name='%s_%s_statistics' % info),
                               )

        urlpatterns += super(MembershipAdmin, self).get_urls()

        return urlpatterns

    def add_to_menu(self, links):
        name, link, children = links['UserAdminExt']
        children['MembershipAdmin'] =  (_('Memberships'), reverse_lazy('admin:kitamembership_membership_statistics'))

        return links

    def remove_from_menu(self, links):
        del links['UserAdminExt'][2]['MembershipAdmin']

        return links

site.register(Membership, MembershipAdmin)

class YearlyRateAdmin(admin.ModelAdmin):
    list_display = ('year', 'rate')

site.register(YearlyRate, YearlyRateAdmin)

class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 0