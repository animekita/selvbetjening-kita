from django.contrib import admin

from selvbetjening.core.selvadmin.admin import site

from models import Achievement, AchievementGroup, Award

class AchievementInline(admin.TabularInline):
    model = Achievement
    extra = 0

class AchievementGroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = [AchievementInline,]

site.register(AchievementGroup, AchievementGroupAdmin)

class AwardInline(admin.TabularInline):
    model = Award
    extra = 0
    raw_id_fields = ('user',)

class AchievementAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = [AwardInline,]

site.register(Achievement, AchievementAdmin)

site.register(Award)