from selvbetjening.sadmin.base.sadmin import SModelAdmin, STabularInline, main_menu

from models import Position, PositionHistory, Tournament, Winner

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

        tournament_admin = TournamentAdmin()
        tournament_admin.sadmin_menu = self.sadmin_menu
        self.sadmin_menu.register(tournament_admin.page_root)
        tournament_admin.page_root.parent = self.page_root

        urlpatterns = super(PositionAdmin, self).get_urls()

        urlpatterns = patterns('',
            (r'^tournaments/', include(tournament_admin.urls)),
        ) + urlpatterns

        return urlpatterns

class WinnerInline(STabularInline):
    model = Winner
    exclude = ('award',)
    raw_id_fields = ('user', 'event',)

class TournamentAdmin(SModelAdmin):
    class Meta:
        app_name = 'achievements'
        name = 'tournament'
        model = Tournament

        display_name = 'Tournament'
        display_name_plural = 'Tournaments'

    list_display = ('name',)
    search_fields = ('name',)
    exclude = ('achievement', )
    inlines = [WinnerInline,]