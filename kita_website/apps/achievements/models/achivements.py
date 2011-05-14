from django.db import models
from django.contrib.auth.models import User

class AchivementGroup(models.Model):
    slug = models.SlugField(primary_key=True)

    name = models.CharField(max_length=255)

    class Meta:
        app_label = 'achievements'

    class Default:
        @staticmethod
        def events(orm=None):
            if orm is None:
                orm = AchivementGroup

            group, created = orm.objects.get_or_create(
                slug='events', defaults={'name' : 'Arrangementer'})

            return group

        @staticmethod
        def general(orm=None):
            if orm is None:
                orm = AchivementGroup

            group, created = orm.objects.get_or_create(
                slug='general', defaults={'name' : 'Overordnet'})

            return group

    def __unicode__(self):
        return self.name

class Achivement(models.Model):
    slug = models.SlugField(primary_key=True)

    group = models.ForeignKey(AchivementGroup)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'achievements'

    class Default:
        @staticmethod
        def member_of_kita(orm=None, group_orm=None):
            if orm is None:
                orm = Achivement

            achievement, created = orm.objects.get_or_create(
                slug='member_of_kita', defaults={'name' : 'Medlem af Anime Kita',
                                                 'group' : AchivementGroup.Default.general(group_orm)})

            return achievement

class Award(models.Model):
    achievement = models.ForeignKey(Achivement)
    user = models.ForeignKey(User)

    note = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'achievements'

