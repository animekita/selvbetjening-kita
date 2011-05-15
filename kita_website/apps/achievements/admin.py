from selvbetjening.sadmin.base.sadmin import SModelAdmin, STabularInline, main_menu

from models import Position, PositionHistory, Turnament, Winner

class PositionHistoryInline(STabularInline):
    model = PositionHistory
    exclude = ('award', )
    raw_id_fields = ('user', )

class PositionAdmin(SModelAdmin):
    class Meta:
        app_name = 'achievements'
        name = 'position'
        model = Position

        display_name = 'Position'
        display_name_plural = 'Positions'

    list_display = ('name', 'monitor_group')
    search_fields = ('name',)
    exclude = ('achievement', )
    inlines = [PositionHistoryInline,]

    def _init_navigation(self):
        super(PositionAdmin, self)._init_navigation()

        main_menu.register(self.page_root, 'Achievements')

    def get_urls(self):
        from django.conf.urls.defaults import patterns, url, include

        turnament_admin = TurnamentAdmin()
        turnament_admin.sadmin_menu = self.sadmin_menu
        self.sadmin_menu.register(turnament_admin.page_root)
        turnament_admin.page_root.parent = self.page_root

        urlpatterns = super(PositionAdmin, self).get_urls()

        urlpatterns = patterns('',
            (r'^turnaments/', include(turnament_admin.urls)),
        ) + urlpatterns

        return urlpatterns

class WinnerInline(STabularInline):
    model = Winner
    exclude = ('award',)
    raw_id_fields = ('user', 'event',)

class TurnamentAdmin(SModelAdmin):
    class Meta:
        app_name = 'achievements'
        name = 'turnament'
        model = Turnament

        display_name = 'Turnament'
        display_name_plural = 'Turnaments'

    list_display = ('name',)
    search_fields = ('name',)
    exclude = ('achievement', )
    inlines = [WinnerInline,]