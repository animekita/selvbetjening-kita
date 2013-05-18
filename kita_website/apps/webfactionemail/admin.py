from django.contrib.auth.models import User

from selvbetjening.sadmin.base.sadmin import SModelAdmin, STabularInline, main_menu

from models import Email, MailingList


class EmailAdmin(SModelAdmin):
    class Meta:
        app_name = 'webfactionemail'
        name = 'email'
        model = Email

        display_name = 'E-mail'
        display_name_plural = 'E-mails'

    change_readonly = ['email_prefix']

    fieldsets = (
        (None, {
            'fields': ('email_prefix', 'forwards', 'forwards_group', 'forwards_other')
        }),
    )

    actions_on_top = False
    filter_horizontal = ['forwards', 'forwards_group']

    def forwards(instance):
        return ', '.join([user.username for user in instance.forwards.all()])

    def groups(instance):
        return ', '.join([user.username for user in User.objects.filter(groups__in=instance.forwards_group.all())])

    list_display = ('email', forwards, groups, 'forwards_other', 'marked_for_deletion')
    search_fields = ('email', 'forwards', 'forwards_other')

    def _init_navigation(self):
        super(EmailAdmin, self)._init_navigation()

        main_menu.register(self.page_root, 'E-mail Forwards')

    def get_urls(self):
        from django.conf.urls import patterns, url, include

        mailinglist_admin = MailingListAdmin()
        mailinglist_admin.page_root.parent = self.page_root
        mailinglist_admin.module_menu = self.module_menu
        self.module_menu.register(mailinglist_admin.page_root)

        urlpatterns = super(EmailAdmin, self).get_urls()

        urlpatterns = patterns('',
            (r'^mailinglists/', include(mailinglist_admin.urls)),
        ) + urlpatterns

        return urlpatterns


class MailingListAdmin(SModelAdmin):
    class Meta:
        app_name = 'webfactionemail'
        name = 'mailinglist'
        model = MailingList

        display_name = 'Mailinglist'
        display_name_plural = 'Mailinglists'

        default_views = ('list', 'change')

    change_readonly = ['email']

    fieldsets = (
        (None, {
            'fields': ('email', 'forwards', 'forwards_group', 'forwards_other')
        }),
    )

    filter_horizontal = ['forwards', 'forwards_group']

    def forwards(instance):
        return ', '.join([user.username for user in instance.forwards.all()])

    list_display = ('email', forwards, 'forwards_other')
    search_fields = ('email', 'forwards', 'forwards_other')


