from selvbetjening.sadmin.base.sadmin import SModelAdmin, main_menu

from models import Order

class OrderAdmin(SModelAdmin):
    class Meta:
        app_name = 'comicparty'
        name = 'order'
        model = Order
        
        display_name = 'Comic Party Order'
        display_name_plural = 'Comic Party Orders'

    list_display = ('user', 'timestamp')
    search_fields = ('user',)
    
    def _init_navigation(self):
        super(OrderAdmin, self)._init_navigation()
        
        main_menu.register(self.page_root, 'Comic Party')
