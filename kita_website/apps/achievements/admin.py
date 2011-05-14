from django.contrib import admin

from selvbetjening.core.selvadmin.admin import site

from models import Achivement, AchivementGroup, Award

class AchivementInline(admin.TabularInline):
    model = Achivement
    extra = 0

class AchivementGroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = [AchivementInline,]

site.register(AchivementGroup, AchivementGroupAdmin)

class AwardInline(admin.TabularInline):
    model = Award
    extra = 0
    raw_id_fields = ('user',)

class AchivementAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = [AwardInline,]

site.register(Achivement, AchivementAdmin)

site.register(Award)