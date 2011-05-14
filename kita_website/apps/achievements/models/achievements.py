from django.db import models
from django.contrib.auth.models import User

class AchievementGroup(models.Model):
    slug = models.SlugField(primary_key=True)

    name = models.CharField(max_length=255)

    class Meta:
        app_label = 'achievements'

    class Default:
        @staticmethod
        def events(orm=None):
            if orm is None:
                orm = AchievementGroup

            group, created = orm.objects.get_or_create(
                slug='events', defaults={'name' : 'Arrangementer'})

            return group

        @staticmethod
        def general(orm=None):
            if orm is None:
                orm = AchievementGroup

            group, created = orm.objects.get_or_create(
                slug='general', defaults={'name' : 'Overordnet'})

            return group

    def __unicode__(self):
        return self.name

class Achievement(models.Model):
    slug = models.SlugField(primary_key=True)

    group = models.ForeignKey(AchievementGroup)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'achievements'

    class Default:
        @staticmethod
        def member_of_kita(orm=None, group_orm=None):
            if orm is None:
                orm = Achievement

            achievement, created = orm.objects.get_or_create(
                slug='member_of_kita', defaults={'name' : 'Medlem af Anime Kita',
                                                 'group' : AchievementGroup.Default.general(group_orm)})

            return achievement

class Award(models.Model):
    achievement = models.ForeignKey(Achievement)
    user = models.ForeignKey(User)

    note = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'achievements'

